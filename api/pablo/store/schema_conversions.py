from sqlalchemy.engine import RowMapping

from pablo.internal.model import Image
from pablo.internal.model import ImageVariant
from pablo.internal.model import UrlUpload
from pablo.store.schema import ImagesTable
from pablo.store.schema import ImageVariantsTable
from pablo.store.schema import UrlUploadsTable


def image_from_row(rowMapping: RowMapping) -> Image:
    return Image(
        imageId=rowMapping[ImagesTable.c.imageId],
        createdDate=rowMapping[ImagesTable.c.createdDate],
        updatedDate=rowMapping[ImagesTable.c.updatedDate],
        format=rowMapping[ImagesTable.c.format],
        filename=rowMapping[ImagesTable.c.filename],
        width=rowMapping[ImagesTable.c.width],
        height=rowMapping[ImagesTable.c.height],
        area=rowMapping[ImagesTable.c.area],
    )


def image_variant_from_row(rowMapping: RowMapping) -> ImageVariant:
    return ImageVariant(
        imageVariantId=rowMapping[ImageVariantsTable.c.imageVariantId],
        createdDate=rowMapping[ImageVariantsTable.c.createdDate],
        updatedDate=rowMapping[ImageVariantsTable.c.updatedDate],
        imageId=rowMapping[ImageVariantsTable.c.imageId],
        filename=rowMapping[ImageVariantsTable.c.filename],
        isPreview=rowMapping[ImageVariantsTable.c.isPreview],
        width=rowMapping[ImageVariantsTable.c.width],
        height=rowMapping[ImageVariantsTable.c.height],
        area=rowMapping[ImageVariantsTable.c.area],
    )


def url_upload_from_row(rowMapping: RowMapping) -> UrlUpload:
    return UrlUpload(
        urlUploadId=rowMapping[UrlUploadsTable.c.urlUploadId],
        createdDate=rowMapping[UrlUploadsTable.c.createdDate],
        updatedDate=rowMapping[UrlUploadsTable.c.updatedDate],
        url=rowMapping[UrlUploadsTable.c.url],
        imageId=rowMapping[UrlUploadsTable.c.imageId],
    )
