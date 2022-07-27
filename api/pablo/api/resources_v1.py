from pydantic import BaseModel

from pablo.internal.model import SERVING_URL
from pablo.internal.model import Image
from pablo.internal.model import ImageVariant


class ApiImage(BaseModel):
    imageId: str
    width: int
    height: int
    format: str
    url: str
    resizableUrl: str

    @classmethod
    def from_model(cls, model: Image):
        return cls(
            imageId=model.imageId,
            width=model.width,
            height=model.height,
            format=model.format,
            # TODO(krishan711): these would be better using servingUrl instead of hard-coding
            url=f'{SERVING_URL}/static/images/{model.imageId}/{model.filename}',
            resizableUrl=f'{SERVING_URL}/v1/images/{model.imageId}/go',
        )


class ApiImageVariant(BaseModel):
    imageId: str
    imageVariantId: str
    width: int
    height: int

    @classmethod
    def from_model(cls, model: ImageVariant):
        return cls(
            imageId=model.imageId,
            imageVariantId=model.imageVariantId,
            width=model.width,
            height=model.height,
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
