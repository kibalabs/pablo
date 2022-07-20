import uuid
from io import BytesIO
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple

import magic
from core import logging
from core.exceptions import BadRequestException
from core.exceptions import NotFoundException
from core.exceptions import PermanentRedirectException
from core.queues.sqs_message_queue import SqsMessageQueue
from core.requester import Requester
from core.requester import ResponseException
from core.s3_manager import S3Manager
from core.store.retriever import Direction
from core.store.retriever import IntegerFieldFilter
from core.store.retriever import Order
from core.store.retriever import StringFieldFilter
from core.util import file_util
from PIL import Image as PILImage
from starlette.responses import Response

from pablo.internal.ipfs_requester import IpfsRequester
from pablo.internal.messages import ResizeImageMessageContent
from pablo.internal.model import CLOUDFRONT_URL
from pablo.internal.model import IMAGE_FORMAT_EXTENSION_MAP
from pablo.internal.model import IMAGE_FORMAT_PIL_TYPE_MAP
from pablo.internal.model import Image
from pablo.internal.model import ImageFormat
from pablo.internal.model import ImageVariant
from pablo.store.retriever import Retriever
from pablo.store.saver import Saver
from pablo.store.schema import ImageVariantsTable

_TARGET_SIZES = [100, 200, 300, 500, 640, 750, 1000, 1080, 1920, 2500]

class PabloManager:

    def __init__(self, retriever: Retriever, saver: Saver, requester: Requester, ipfsRequesters: List[IpfsRequester], workQueue: SqsMessageQueue, s3Manager: S3Manager, bucketName: str, servingUrl: str) -> None:
        self.retriever = retriever
        self.saver = saver
        self.requester = requester
        self.ipfsRequesters = ipfsRequesters
        self.workQueue = workQueue
        self.s3Manager = s3Manager
        self.bucketName = bucketName
        self.servingUrl = servingUrl
        self.ipfsS3Path = f's3://{self.bucketName}/static/ipfs'
        self.imagesS3Path = f's3://{self.bucketName}/static/images'
        self.ipfsServingUrl = f'{servingUrl}/static/ipfs'
        self.imagesServingUrl = f'{servingUrl}/static/images'

    # async def list_images(self) -> Sequence[Image]:
    #     pass

    async def get_image(self, imageId: str) -> Image:
        image = await self.retriever.get_image(imageId=imageId)
        return image

    async def list_image_variants(self, imageId: str) -> Sequence[ImageVariant]:
        imageVariants = await self.retriever.list_image_variants(fieldFilters=[
            StringFieldFilter(fieldName=ImageVariantsTable.c.imageId.key, eq=imageId),
        ])
        return imageVariants

    async def get_image_variant(self, imageId: str, imageVariantId: str) -> ImageVariant:
        image = await self.retriever.get_image_variant(imageVariantId=imageVariantId)
        if image.imageId != imageId:
            raise NotFoundException()
        return image

    async def go_to_image(self, imageId: str, width: Optional[int] = None, height: Optional[int] = None) -> str:
        image = await self.retriever.get_image(imageId=imageId)
        filters = [StringFieldFilter(fieldName=ImageVariantsTable.c.imageId.key, eq=imageId)]
        if width is not None:
            filters.append(IntegerFieldFilter(fieldName=ImageVariantsTable.c.width.key, gte=width))
        if height is not None:
            filters.append(IntegerFieldFilter(fieldName=ImageVariantsTable.c.height.key, gte=height))
        imageVariants = await self.retriever.list_image_variants(
            fieldFilters=filters,
            orders=[Order(fieldName=ImageVariantsTable.c.area.key, direction=Direction.ASCENDING)],
            limit=1
        )
        if len(imageVariants) == 0:
            raise PermanentRedirectException(location=f'{self.imagesServingUrl}/{imageId}/{image.filename}')
        raise PermanentRedirectException(location=f'{self.imagesServingUrl}/{imageId}/{imageVariants[0].filename}')

    # async def generate_image_upload(self, filename: str) -> S3PresignedUpload:
    #     presignedUpload = await self.s3Manager.generate_presigned_upload(target=f's3://{self.bucketName}/uploads/${{{filename}}}', timeLimit=60, sizeLimit=file_util.MEGABYTE * 10, accessControl='public-read', cacheControl=file_util.CACHE_CONTROL_FINAL_FILE)
    #     return presignedUpload

    async def upload_image_url(self, url: str) -> str:
        try:
            urlUpload = await self.retriever.get_url_upload_by_url(url=url)
        except NotFoundException:
            urlUpload = None
        if urlUpload:
            return urlUpload.imageId
        imageId = str(uuid.uuid4()).replace('-', '')
        localFilePath = f'./tmp/{imageId}/download-for-upload'
        resolvedUrl = url
        if url.startswith('ipfs://'):
            cid = url.replace('ipfs://', '')
            await self.load_ipfs(cid=cid)
            resolvedUrl = f'{CLOUDFRONT_URL}/static/ipfs/{cid}'
        response = await self.requester.get(url=resolvedUrl, outputFilePath=localFilePath)
        imageFormat = response.headers.get('content-type')
        if imageFormat and imageFormat not in IMAGE_FORMAT_EXTENSION_MAP:
            raise BadRequestException(f'Unsupported image format')
        await self.s3Manager.upload_file(filePath=localFilePath, targetPath=f'{self.imagesS3Path}/{imageId}/original', accessControl='public-read', cacheControl=file_util.CACHE_CONTROL_FINAL_FILE)
        await file_util.remove_file(filePath=localFilePath)
        # TODO(krishan711): can we use deferred here?
        await self.save_image(imageId=imageId, imageFormat=imageFormat)
        await self.saver.create_url_upload(url=url, imageId=imageId)
        return imageId

    async def save_image_deferred(self, imageId: str, imageFormat: Optional[str]) -> None:
        # TODO(krishan711): implement this
        pass

    async def save_image(self, imageId: str, imageFormat: Optional[str]) -> None:
        try:
            image = await self.retriever.get_image(imageId=imageId)
        except NotFoundException:
            image = None
        if image:
            logging.info(f'Skipping saving image that already exists: {imageId}')
            return
        imageContent = await self.s3Manager.read_file(sourcePath=f'{self.imagesS3Path}/{imageId}/original')
        if not imageFormat:
            imageFormat = magic.from_buffer(imageContent)
        if imageFormat not in IMAGE_FORMAT_EXTENSION_MAP:
            raise BadRequestException(f'Unsupported image format')
        filename = f'original.{IMAGE_FORMAT_EXTENSION_MAP[imageFormat]}'
        width = 0
        height = 0
        if imageFormat != ImageFormat.SVG:
            with PILImage.open(BytesIO(imageContent)) as pilImage:
                width, height = pilImage.size
        await self.s3Manager.write_file(content=imageContent, targetPath=f'{self.imagesS3Path}/{imageId}/{filename}', accessControl='public-read', cacheControl=file_util.CACHE_CONTROL_FINAL_FILE)
        await self.saver.create_image(imageId=imageId, format=imageFormat, filename=filename, width=width, height=height, area=(width * height))
        await self.resize_image_deferred(imageId=imageId)

    async def resize_image_deferred(self, imageId: str) -> None:
        await self.workQueue.send_message(message=ResizeImageMessageContent(imageId=imageId).to_message())

    @staticmethod
    def _resize_image_content(imageContent: bytes, imageFormat: ImageFormat, width: int, height: int) -> Image:
        content = BytesIO()
        if imageFormat in IMAGE_FORMAT_PIL_TYPE_MAP:
            with PILImage.open(fp=BytesIO(imageContent)) as pilImage:
                newPilImage = pilImage.resize(size=(width, height))
                newPilImage.save(fp=content, format=IMAGE_FORMAT_PIL_TYPE_MAP[imageFormat])
        else:
            raise BadRequestException(message=f'Cannot process image with format {imageFormat}')
        return content.getvalue()

    async def resize_image(self, imageId: str) -> None:
        image = await self.retriever.get_image(imageId=imageId)
        imageContent = await self.s3Manager.read_file(sourcePath=f'{self.imagesS3Path}/{imageId}/original')
        extension = IMAGE_FORMAT_EXTENSION_MAP[image.format]
        imageVariants = await self.list_image_variants(imageId=imageId)
        existingSizes = set([(imageVariant.width, imageVariant.height) for imageVariant in imageVariants])
        targetSizes: Set[Tuple[int, int]] = set()
        for targetSize in _TARGET_SIZES:
            if image.width >= targetSize:
                targetSizes.add((targetSize, int(targetSize * (image.height / image.width))))
            if image.height >= targetSize:
                targetSizes.add((int(targetSize * (image.width / image.height)), targetSize))
        for targetWidth, targetHeight in (targetSizes - existingSizes):
            # TODO(krishan711): check if the variant already exists
            logging.info(f'Resizing to ({targetWidth}, {targetHeight})')
            resizedImageContent = self._resize_image_content(imageContent=imageContent, imageFormat=image.format, width=targetWidth, height=targetHeight)
            variantFileName = f'{targetWidth}-{targetHeight}.{extension}'
            await self.s3Manager.write_file(content=resizedImageContent, targetPath=f'{self.imagesS3Path}/{imageId}/{variantFileName}', accessControl='public-read', cacheControl=file_util.CACHE_CONTROL_FINAL_FILE)
            await self.saver.create_image_variant(imageId=imageId, filename=variantFileName, width=targetWidth, height=targetHeight, area=(targetWidth * targetHeight))

    async def get_ipfs_head(self, cid: str) -> Response:
        try:
            headers = await self.s3Manager.head_file(filePath=f'{self.ipfsS3Path}/{cid}')
        except NotFoundException:
            headers = None
        if headers is None:
            exceptions = []
            response = None
            for ipfsRequester in self.ipfsRequesters:
                try:
                    response = await ipfsRequester.make_request(method='HEAD', url=f'ipfs://{cid}', timeout=60)
                    break
                except ResponseException as exception:
                    exceptions.append(exception)
            if not response:
                raise exceptions[-1]
            headers = response.headers
        return Response(content=None, headers=headers)

    async def get_ipfs(self, cid: str) -> Response:
        await self.load_ipfs(cid=cid)
        raise PermanentRedirectException(location=f'{self.ipfsServingUrl}/{cid}')

    async def load_ipfs(self, cid: str) -> None:
        isExisting = await self.s3Manager.check_file_exists(filePath=f'{self.ipfsS3Path}/{cid}')
        if isExisting:
            return None
        localFilePath = f'./tmp/{cid.replace("/", "_")}/download-for-upload'
        exceptions = []
        response = None
        for ipfsRequester in self.ipfsRequesters:
            logging.stat(name='IPFS', key=ipfsRequester.ipfsHost, value=1)
            try:
                response = await ipfsRequester.make_request(method='GET', url=f'ipfs://{cid}', outputFilePath=localFilePath, timeout=600)
                break
            except ResponseException as exception:
                logging.stat(name='IPFS-ERROR', key=ipfsRequester.ipfsHost, value=exception.statusCode)
                exceptions.append(exception)
        if not response:
            raise exceptions[-1]
        await self.s3Manager.upload_file(filePath=localFilePath, targetPath=f'{self.ipfsS3Path}/{cid}', accessControl='public-read', cacheControl=file_util.CACHE_CONTROL_FINAL_FILE, contentType=response.headers['Content-Type'])
        await file_util.remove_file(filePath=localFilePath)
