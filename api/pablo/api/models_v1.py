from typing import List

from pydantic import BaseModel

from pablo.internal.model import Image


class ApiImage(BaseModel):
    imageId: str
    width: int
    height: int
    format: str
    url: str

    @classmethod
    def from_model(cls, model: Image):
        return cls(
            imageId=model.imageId,
            width=model.width,
            height=model.height,
            format=model.format,
            url=model.url,
        )

class ApiImageVariant(BaseModel):
    imageId: str
    variantId: str
    width: int
    height: int
    format: str
    url: str

    @classmethod
    def from_model(cls, model: Image):
        return cls(
            imageId=model.imageId,
            variantId=model.variantId,
            width=model.width,
            height=model.height,
            format=model.format,
            url=model.url,
        )

# class ApiPresignedUpload(BaseModel):
#     url: str
#     params: Dict[str, str]

#     @classmethod
#     def from_presigned_upload(cls, presignedUpload: S3PresignedUpload):
#         return cls(
#             url=presignedUpload.url,
#             params={field.name: field.value for field in presignedUpload.fields},
#         )

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
    imageId: str
