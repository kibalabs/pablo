from typing import List

from pydantic import BaseModel

from pablo.resources import ApiImage
from pablo.resources import ApiImageVariant


class ListImagesRequest(BaseModel):
    pass

class ListImagesResponse(BaseModel):
    images: List[ApiImage]

class GetImageRequest(BaseModel):
    pass

class GetImageResponse(BaseModel):
    image: ApiImage

class ListImageVariantsRequest(BaseModel):
    pass

class ListImageVariantsResponse(BaseModel):
    imageVariants: List[ApiImageVariant]

class GetImageVariantRequest(BaseModel):
    pass

class GetImageVariantResponse(BaseModel):
    imageVariant: ApiImageVariant

# class GenerateImageUploadRequest(BaseModel):
#     filename: str

# class GenerateImageUploadResponse(BaseModel):
#     presignedUpload: ApiPresignedUpload

class UploadImageUrlRequest(BaseModel):
    url: str

class UploadImageUrlResponse(BaseModel):
    image: ApiImage
