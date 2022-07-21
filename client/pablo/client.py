

from typing import Sequence

from core.requester import Requester
from core.service_client import ServiceClient

from pablo.resources import ApiImage
from pablo.resources import ApiImageVariant
from pablo.endpoints import GetImageRequest
from pablo.endpoints import GetImageResponse
from pablo.endpoints import GetImageVariantRequest
from pablo.endpoints import GetImageVariantResponse
from pablo.endpoints import ListImageVariantsRequest
from pablo.endpoints import ListImageVariantsResponse
from pablo.endpoints import UploadImageUrlRequest
from pablo.endpoints import UploadImageUrlResponse


class PabloClient(ServiceClient):

    def __init__(self, requester: Requester, baseUrl: str = 'https://pablo-api.kibalabs.com') -> None:
        super().__init__(requester=requester, baseUrl=baseUrl)

    async def get_image(self, imageId: str) -> ApiImage:
        method = 'GET'
        path = f'v1/images/{imageId}'
        request = GetImageRequest()
        response = await self.make_request(method=method, path=path, request=request, responseClass=GetImageResponse)
        return response.image

    async def list_image_variants(self, imageId: str) -> Sequence[ApiImageVariant]:
        method = 'GET'
        path = f'v1/images/{imageId}/variants'
        request = ListImageVariantsRequest()
        response = await self.make_request(method=method, path=path, request=request, responseClass=ListImageVariantsResponse)
        return response.imageVariants

    async def get_image_variant(self, imageId: str, imageVariantId: str) -> ApiImageVariant:
        method = 'GET'
        path = f'v1/images/{imageId}/variants/{imageVariantId}'
        request = GetImageVariantRequest()
        response = await self.make_request(method=method, path=path, request=request, responseClass=GetImageVariantResponse)
        return response.imageVariant

    async def upload_image_url(self, url: str) -> ApiImage:
        method = 'POST'
        path = f'v1/upload-image-url'
        request = UploadImageUrlRequest(url=url)
        response = await self.make_request(method=method, path=path, request=request, responseClass=UploadImageUrlResponse)
        return response.image
