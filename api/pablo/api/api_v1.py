from typing import Optional

from fastapi import APIRouter
from starlette.responses import Response

from pablo.api.endpoints_v1 import GetGoToImageResponse
from pablo.api.endpoints_v1 import GetImageResponse
from pablo.api.endpoints_v1 import GetImageVariantResponse
from pablo.api.endpoints_v1 import ListImageVariantsResponse
from pablo.api.endpoints_v1 import UploadImageUrlRequest
from pablo.api.endpoints_v1 import UploadImageUrlResponse
from pablo.api.resources_v1 import ApiImage
from pablo.api.resources_v1 import ApiImageVariant
from pablo.internal.pablo_manager import PabloManager


def create_api(manager: PabloManager) -> APIRouter:
    router = APIRouter()

    # @router.get('/images', response_model=ListImagesResponse)
    # async def list_images() -> ListImagesResponse: # request: ListImagesRequest
    #     images = await manager.list_images()
    #     return ListImagesResponse(images=[ApiImage.from_model(model=image) for image in images])

    @router.get('/images/{imageId}', response_model=GetImageResponse)
    async def get_image(imageId: str) -> GetImageResponse:
        image = await manager.get_image(imageId=imageId)
        return GetImageResponse(image=ApiImage.from_model(model=image))

    @router.get('/images/{imageId}/variants', response_model=ListImageVariantsResponse)
    async def list_image_variants(imageId: str) -> ListImageVariantsResponse:
        imageVariants = await manager.list_image_variants(imageId=imageId)
        return ListImageVariantsResponse(imageVariants=[ApiImageVariant.from_model(model=imageVariant) for imageVariant in imageVariants])

    @router.get('/images/{imageId}/variants/{imageVariantId}', response_model=GetImageVariantResponse)
    async def get_image_variant(imageId: str, imageVariantId: str) -> GetImageVariantResponse:
        imageVariant = await manager.get_image_variant(imageId=imageId, imageVariantId=imageVariantId)
        return GetImageVariantResponse(imageVariant=ApiImageVariant.from_model(model=imageVariant))

    @router.get('/images/{imageId}/go', response_model=GetGoToImageResponse)
    async def go_to_image(imageId: str, p: Optional[bool] = None, w: Optional[int] = None, h: Optional[int] = None, original: Optional[str] = None) -> GetGoToImageResponse: # pylint: disable=invalid-name
        await manager.go_to_image(imageId=imageId, isPreview=p, width=w, height=h, original=bool(original))
        return GetGoToImageResponse()

    # @router.post('/generate-image-upload', response_model=GenerateImageUploadResponse)
    # async def generate_image_upload(request: GenerateImageUploadRequest):
    #     presignedUpload = await manager.generate_image_upload(filename=request.filename)
    #     return GenerateImageUploadResponse(presignedUpload=ApiPresignedUpload.from_presigned_upload(presignedUpload=presignedUpload))

    @router.post('/upload-image-url', response_model=UploadImageUrlResponse)
    async def upload_image_url(request: UploadImageUrlRequest) -> UploadImageUrlResponse:
        image = await manager.upload_image_url(url=request.url)
        return UploadImageUrlResponse(image=ApiImage.from_model(model=image))

    # TODO(krishan711): how can this be kiba-ified
    @router.get('/ipfs/{cid:path}')
    async def get_ipfs(cid: str) -> Response:
        response = await manager.get_ipfs(cid=cid)
        return response

    # TODO(krishan711): how can this be kiba-ified
    @router.head('/ipfs/{cid:path}')
    async def get_ipfs_head(cid: str) -> Response:
        response = await manager.get_ipfs_head(cid=cid)
        return response

    return router
