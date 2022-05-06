from typing import Mapping

from pablo.internal.model import Image
from pablo.internal.model import ImageVariant
from pablo.internal.model import UrlUpload
from pablo.store.schema import ImagesTable
from pablo.store.schema import ImageVariantsTable
from pablo.store.schema import UrlUploadsTable


def image_from_row(row: Mapping) -> Image:
    return Image(
        imageId=row[ImagesTable.c.imageId],
        createdDate=row[ImagesTable.c.createdDate],
        updatedDate=row[ImagesTable.c.updatedDate],
        format=row[ImagesTable.c.format],
        filename=row[ImagesTable.c.filename],
        width=row[ImagesTable.c.width],
        height=row[ImagesTable.c.height],
        area=row[ImagesTable.c.area],
    )


def image_variant_from_row(row: Mapping) -> ImageVariant:
    return ImageVariant(
        imageVariantId=row[ImageVariantsTable.c.imageVariantId],
        createdDate=row[ImageVariantsTable.c.createdDate],
        updatedDate=row[ImageVariantsTable.c.updatedDate],
        imageId=row[ImageVariantsTable.c.imageId],
        filename=row[ImageVariantsTable.c.filename],
        width=row[ImageVariantsTable.c.width],
        height=row[ImageVariantsTable.c.height],
        area=row[ImageVariantsTable.c.area],
    )


def url_upload_from_row(row: Mapping) -> UrlUpload:
    return UrlUpload(
        urlUploadId=row[UrlUploadsTable.c.urlUploadId],
        createdDate=row[UrlUploadsTable.c.createdDate],
        updatedDate=row[UrlUploadsTable.c.updatedDate],
        url=row[UrlUploadsTable.c.url],
        imageId=row[UrlUploadsTable.c.imageId],
    )
