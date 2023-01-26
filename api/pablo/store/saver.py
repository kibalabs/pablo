from typing import Optional

from core.store.database import DatabaseConnection
from core.store.saver import Saver as CoreSaver
from core.util import date_util

from pablo.internal.model import Image
from pablo.internal.model import ImageVariant
from pablo.internal.model import UrlUpload
from pablo.store.schema import ImagesTable
from pablo.store.schema import ImageVariantsTable
from pablo.store.schema import UrlUploadsTable


class Saver(CoreSaver):

    async def create_image(self, imageId: str, format: str, filename: str, width: int, height: int, area: int, connection: Optional[DatabaseConnection] = None) -> Image:  # pylint: disable=redefined-builtin
        createdDate = date_util.datetime_from_now()
        updatedDate = createdDate
        values = {
            ImagesTable.c.imageId.key: imageId,
            ImagesTable.c.createdDate.key: createdDate,
            ImagesTable.c.updatedDate.key: updatedDate,
            ImagesTable.c.format.key: format,
            ImagesTable.c.filename.key: filename,
            ImagesTable.c.width.key: width,
            ImagesTable.c.height.key: height,
            ImagesTable.c.area.key: area,
        }
        query = ImagesTable.insert().values(values)
        await self._execute(query=query, connection=connection)
        return Image(
            imageId=imageId,
            createdDate=createdDate,
            updatedDate=updatedDate,
            format=format,
            filename=filename,
            width=width,
            height=height,
            area=area,
        )

    async def create_image_variant(self, imageId: str, filename: str, isPreview: bool, width: int, height: int, area: int, connection: Optional[DatabaseConnection] = None) -> ImageVariant:
        createdDate = date_util.datetime_from_now()
        updatedDate = createdDate
        values = {
            ImageVariantsTable.c.createdDate.key: createdDate,
            ImageVariantsTable.c.updatedDate.key: updatedDate,
            ImageVariantsTable.c.imageId.key: imageId,
            ImageVariantsTable.c.filename.key: filename,
            ImageVariantsTable.c.isPreview.key: isPreview,
            ImageVariantsTable.c.width.key: width,
            ImageVariantsTable.c.height.key: height,
            ImageVariantsTable.c.area.key: area,
        }
        query = ImageVariantsTable.insert().values(values)
        result = await self._execute(query=query, connection=connection)
        imageVariantId = result.inserted_primary_key[0]
        return ImageVariant(
            imageVariantId=imageVariantId,
            createdDate=createdDate,
            updatedDate=updatedDate,
            imageId=imageId,
            filename=filename,
            isPreview=isPreview,
            width=width,
            height=height,
            area=area,
        )

    async def create_url_upload(self, url: str, imageId: str, connection: Optional[DatabaseConnection] = None) -> UrlUpload:
        createdDate = date_util.datetime_from_now()
        updatedDate = createdDate
        values = {
            UrlUploadsTable.c.createdDate.key: createdDate,
            UrlUploadsTable.c.updatedDate.key: updatedDate,
            UrlUploadsTable.c.url.key: url,
            UrlUploadsTable.c.imageId.key: imageId,
        }
        query = UrlUploadsTable.insert().values(values)
        result = await self._execute(query=query, connection=connection)
        urlUploadId = result.inserted_primary_key[0]
        return UrlUpload(
            urlUploadId=urlUploadId,
            createdDate=createdDate,
            updatedDate=updatedDate,
            url=url,
            imageId=imageId,
        )
