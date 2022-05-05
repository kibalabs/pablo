import dataclasses
import datetime

class ImageFormat:
    JPG = "image/jpg"
    PNG = "image/png"
    WEBP = "image/webp"

IMAGE_FORMAT_MAP = {
    ImageFormat.JPG: 'jpg',
    ImageFormat.PNG: 'png',
    ImageFormat.WEBP: 'webp',
}


@dataclasses.dataclass
class ImageData:
    content: bytes
    width: int
    height: int
    format: str


@dataclasses.dataclass
class UrlUpload:
    urlUploadId: str
    createdDate: datetime.datetime
    updatedDate: datetime.datetime
    url: str
    imageId: str


@dataclasses.dataclass
class Image:
    imageId: str
    createdDate: datetime.datetime
    updatedDate: datetime.datetime
    format: str
    filename: str
    width: int
    height: int
    area: int


@dataclasses.dataclass
class ImageVariant:
    imageVariantId: str
    createdDate: datetime.datetime
    updatedDate: datetime.datetime
    imageId: str
    filename: str
    width: int
    height: int
    area: int
