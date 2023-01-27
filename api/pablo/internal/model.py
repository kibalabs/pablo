import dataclasses
import datetime
from typing import Optional

CLOUDFRONT_URL = 'https://d35ci2i0uce4j6.cloudfront.net'
SERVING_URL = 'https://pablo-images.kibalabs.com'


class ImageFormat:
    JPG = "image/jpg"
    PNG = "image/png"
    WEBP = "image/webp"
    GIF = "image/gif"
    SVG = "image/svg+xml"


IMAGE_FORMAT_EXTENSION_MAP = {
    ImageFormat.JPG: 'jpg',
    ImageFormat.PNG: 'png',
    ImageFormat.WEBP: 'webp',
    ImageFormat.GIF: 'gif',
    ImageFormat.SVG: 'svg',
}

IMAGE_FORMAT_PIL_TYPE_MAP = {
    ImageFormat.JPG: 'JPEG',
    ImageFormat.PNG: 'PNG',
    ImageFormat.WEBP: 'WEBP',
    ImageFormat.GIF: 'gif',
}

ANIMATED_IMAGE_FORMATS = {
    ImageFormat.GIF,
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
    previewFilename: Optional[str]
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
    isPreview: bool
    width: int
    height: int
    area: int
