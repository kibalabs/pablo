

from typing import Sequence
from pablo.api.endpoints_v1 import GetImageRequest, GetImageResponse, GetImageVariantRequest, GetImageVariantResponse, ListImageVariantsRequest, ListImageVariantsResponse, UploadImageUrlRequest, UploadImageUrlResponse
from core.requester import Requester
from core.service_client import ServiceClient

from pablo.api.resources_v1 import ApiImage, ApiImageVariant


class PabloClient(ServiceClient):

    def __init__(self, requester: Requester, baseUrl: str = 'https://pablo-api.kibalabs.com/v1') -> None:
        super.__init__(requester, baseUrl)

    async def get_image(self, imageId: str) -> ApiImage:
        method = 'GET'
        path = f'/images/{imageId}'
        request = GetImageRequest()
        response = await self.make_request(method=method, path=path, request=request, responseClass=GetImageResponse)
        return response.image

    async def list_image_variants(self, imageId: str) -> Sequence[ApiImageVariant]:
        method = 'GET'
        path = f'/images/{imageId}/variants'
        request = ListImageVariantsRequest()
        response = await self.make_request(method=method, path=path, request=request, responseClass=ListImageVariantsResponse)
        return response.imageVariants

    async def get_image_variant(self, imageId: str, imageVariantId: str) -> ApiImageVariant:
        method = 'GET'
        path = f'/images/{imageId}/variants/{imageVariantId}'
        request = GetImageVariantRequest()
        response = await self.make_request(method=method, path=path, request=request, responseClass=GetImageVariantResponse)
        return response.imageVariant

    async def upload_image_url(self, url: str) -> str:
        method = 'GET'
        path = f'/upload-image-url'
        request = UploadImageUrlRequest(url=url)
        response = await self.make_request(method=method, path=path, request=request, responseClass=UploadImageUrlResponse)
        return response.imageId
