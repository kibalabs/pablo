import dataclasses
import datetime

CLOUDFRONT_URL = 'https://d35ci2i0uce4j6.cloudfront.net'


class ImageFormat:
    JPG = "image/jpg"
    PNG = "image/png"
    WEBP = "image/webp"
    SVG = "image/svg+xml"


IMAGE_FORMAT_EXTENSION_MAP = {
    ImageFormat.JPG: 'jpg',
    ImageFormat.PNG: 'png',
    ImageFormat.WEBP: 'webp',
    ImageFormat.SVG: 'svg',
}

IMAGE_FORMAT_PIL_TYPE_MAP = {
    ImageFormat.JPG: 'JPEG',
    ImageFormat.PNG: 'PNG',
    ImageFormat.WEBP: 'WEBP',
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
