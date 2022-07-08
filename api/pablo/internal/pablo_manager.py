from ctypes import Union
from typing import Dict, List, Optional
from typing import Sequence
import json
import os
import urllib.parse as urlparse
from io import IOBase
from typing import IO
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

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
from starlette.responses import Response
from typing import Union

import httpx

from core import logging
from core.util import dict_util
from core.util import file_util
from core.util.typing_util import JSON

from core.requester import FileContent, KibaResponse

from pablo.internal.model import IMAGE_FORMAT_MAP
from pablo.internal.model import Image
from pablo.internal.model import ImageVariant
from pablo.store.retriever import Retriever
from pablo.store.saver import Saver
from pablo.store.schema import ImageVariantsTable

# ipfs://QmPpuVyyzvsTidhALUZZYdJfxRsDYVZRH1eYZ9fUeZxaea/3966

class IpfsRequester(Requester):

    def __init__(self, ipfsPrefix: str, headers: Optional[Dict[str, str]] = None, shouldFollowRedirects: bool = True):
        super().__init__(headers=headers, shouldFollowRedirects=shouldFollowRedirects)
        self.ipfsPrefix = ipfsPrefix
        
    async def make_request(self, method: str, url: str, dataDict: Optional[JSON] = None, data: Optional[bytes] = None, formDataDict: Optional[Dict[str, Union[str, FileContent]]] = None, formFiles: Optional[Sequence[Tuple[str, Tuple[str, FileContent]]]] = None, timeout: Optional[int] = 10, headers: Optional[Dict[str, str]] = None, outputFilePath: Optional[str] = None) -> KibaResponse:
        if url.startswith('ipfs://'):
            url = url.replace('ipfs://', self.ipfsPrefix, 1)
        return await super().make_request(method=method, url=url, dataDict=dataDict, data=data, formDataDict=formFiles, formFiles=formFiles, timeout=timeout, headers=headers, outputFilePath=outputFilePath)

IPFS_PROVIDER_PREFIXES = [
    IpfsRequester(ipfsPrefix='https://ipfs.io/ipfs'),
    IpfsRequester(ipfsPrefix='https://ipfs.infura.io/ipfs/'),
    IpfsRequester(ipfsPrefix='https://gateway.pinata.cloud/ipfs/'),
    IpfsRequester(ipfsPrefix='https://kibalabs.mypinata.cloud/ipfs/')
]

IPFS_PROVIDER_PREFIXES = [
    'https://ipfs.io/ipfs/',
    'https://ipfs.infura.io/ipfs/',
    'https://gateway.pinata.cloud/ipfs/',
    'https://kibalabs.mypinata.cloud/ipfs/'
]

class PabloManager:

    def __init__(self, retriever: Retriever, saver: Saver, requester: Requester, ipfsRequesters: List[IpfsRequester], workQueue: SqsMessageQueue, s3Manager: S3Manager, bucketName: str, servingUrl: str) -> None:
        self.retriever = retriever
        self.saver = saver
        self.requester = requester
        self.ipfsRequesters = IPFS_PROVIDER_PREFIXES
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
            raise NotFoundException(message=f'Image {imageId} not found')
        # TODO(krishan711): this should return the original in the case where nothing else is found
        raise PermanentRedirectException(location=f'{self.imagesServingUrl}/{imageVariants[0].imageId}/{imageVariants[0].filename}')

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
        imageId = 'test' #str(uuid.uuid4()).replace('-', '')
        # TODO(krishan711): use load_ipfs for ipfs urls
        localFilePath = f'./tmp/{imageId}/download-for-upload'
        response = await self.requester.get(url=url, outputFilePath=localFilePath)
        imageFormat = response.headers.get('content-type')
        if imageFormat and imageFormat not in IMAGE_FORMAT_MAP:
            raise BadRequestException(f'Unsupported image format')
        await self.s3Manager.upload_file(filePath=localFilePath, targetPath=f'{self.imagesS3Path}/{imageId}/original', accessControl='public-read', cacheControl=file_util.CACHE_CONTROL_FINAL_FILE)
        await file_util.remove_file(filePath=localFilePath)
        await self.saver.create_url_upload(url=url, imageId=imageId)
        # TODO(krishan711): can we use deferred here?
        await self.save_image(imageId=imageId, imageFormat=imageFormat)
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
        localFilePath = f'./tmp/{imageId}/download-for-save'
        await self.s3Manager.download_file(sourcePath=f'{self.imagesS3Path}/{imageId}/original', filePath=localFilePath)
        # TODO(krishan711): get the image format
        if not imageFormat:
            imageFormat = 'xyz'
        filename = f'original.{IMAGE_FORMAT_MAP[imageFormat]}'
        # TODO(krishan711): get the image size
        width = 0
        height = 0
        await self.saver.create_image(imageId=imageId, format=imageFormat, filename=filename, width=width, height=height, area=(width * height))
        await self.s3Manager.upload_file(filePath=localFilePath, targetPath=f'{self.imagesS3Path}/{imageId}/{filename}', accessControl='public-read', cacheControl=file_util.CACHE_CONTROL_FINAL_FILE)
        await file_util.remove_file(filePath=localFilePath)
        # TODO(krishan711): add a task to resize the image

    async def resize_image_deferred(self, imageId: str) -> None:
        # TODO(krishan711): implement this
        pass

    async def resize_image(self, imageId: str) -> None:
        pass
    #     image = None
    #     for targetSize in _TARGET_SIZES:
    #         if image.size.width >= targetSize:
    #             # TODO(krishan711): check if the image already exists and skip if it does
    #             resizedImage = await self._resize_image(image=image, size=ImageSize(width=targetSize, height=targetSize * (image.size.height / image.size.width)))
    #             resizedFilename = f'./tmp/{uuid.uuid4()}'
    #             await self._save_image_to_file(image=resizedImage, fileName=resizedFilename)
    #             await self.s3Manager.upload_file(filePath=resizedFilename, targetPath=f'{_BUCKET}/{imageId}/widths/{targetSize}', accessControl='public-read', cacheControl=_CACHE_CONTROL_FINAL_FILE)
    #         if image.size.height >= targetSize:
    #             resizedImage = await self._resize_image(image=image, size=ImageSize(width=targetSize * (image.size.width / image.size.height), height=targetSize))
    #             resizedFilename = f'./tmp/{uuid.uuid4()}'
    #             await self._save_image_to_file(image=resizedImage, fileName=resizedFilename)
    #             await self.s3Manager.upload_file(filePath=resizedFilename, targetPath=f'{_BUCKET}/{imageId}/heights/{targetSize}', accessControl='public-read', cacheControl=_CACHE_CONTROL_FINAL_FILE)
    #     return imageId

    async def _response(self, cid):
        idx = 0
        while idx <= len(IPFS_PROVIDER_PREFIXES):
            try:
                providerResponse = await self.requester.make_request(method='HEAD', url=f'{IPFS_PROVIDER_PREFIXES[idx]}{cid}', timeout=600)
            except ResponseException:
                #Not sure what to do, I want to go to the next index in the prefixes
                idx += 1

            if providerResponse.status_code == 200:
                return providerResponse
        return providerResponse


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
                    response = await ipfsRequester.make_request(method='HEAD', url=f'{cid}', timeout=60)
                    break
                except ResponseException as exception:
                    exceptions.append(exception)
            if not response:
                raise exceptions[-1]
            headers = response.headers
        return Response(content=None, headers=headers)

    async def get_ipfs(self, cid: str) -> Response:
        isExisting = await self.s3Manager.check_file_exists(filePath=f'{self.ipfsS3Path}/{cid}')
        if not isExisting:
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
            try:
                response = await ipfsRequester.make_request(method='HEAD', url=f'https://ipfs.io/ipfs/{cid}', timeout=60)
                break
            except ResponseException as exception:
                exceptions.append(exception)
        if not response:
            raise exceptions[-1]
        await self.s3Manager.upload_file(filePath=localFilePath, targetPath=f'{self.ipfsS3Path}/{cid}', accessControl='public-read', cacheControl=file_util.CACHE_CONTROL_FINAL_FILE, contentType=response.headers['Content-Type'])
        await file_util.remove_file(filePath=localFilePath)
