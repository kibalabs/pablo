from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
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

if TYPE_CHECKING:
    from sqlalchemy.sql._typing import _DMLColumnArgument
else:
    _DMLColumnArgument = Any

_EMPTY_STRING = '_EMPTY_STRING'
_EMPTY_OBJECT = '_EMPTY_OBJECT'

CreateRecordDict = Dict[_DMLColumnArgument, Any]  # type: ignore[misc]
UpdateRecordDict = Dict[_DMLColumnArgument, Any]  # type: ignore[misc]

class Saver(CoreSaver):

    async def create_image(self, imageId: str, format: str, filename: str, previewFilename: Optional[str], width: int, height: int, area: int, connection: Optional[DatabaseConnection] = None) -> Image:  # pylint: disable=redefined-builtin
        createdDate = date_util.datetime_from_now()
        updatedDate = createdDate
        values: CreateRecordDict = {
            ImagesTable.c.imageId.key: imageId,
            ImagesTable.c.createdDate.key: createdDate,
            ImagesTable.c.updatedDate.key: updatedDate,
            ImagesTable.c.format.key: format,
            ImagesTable.c.filename.key: filename,
            ImagesTable.c.previewFilename.key: previewFilename,
            ImagesTable.c.width.key: width,
            ImagesTable.c.height.key: height,
            ImagesTable.c.area.key: area,
        }
        query = ImagesTable.insert().values(values).returning(ImagesTable.c.imageId)
        await self._execute(query=query, connection=connection)
        return Image(
            imageId=imageId,
            createdDate=createdDate,
            updatedDate=updatedDate,
            format=format,
            filename=filename,
            previewFilename=previewFilename,
            width=width,
            height=height,
            area=area,
        )

    async def create_image_variant(self, imageId: str, filename: str, isPreview: bool, width: int, height: int, area: int, connection: Optional[DatabaseConnection] = None) -> ImageVariant:
        createdDate = date_util.datetime_from_now()
        updatedDate = createdDate
        values: CreateRecordDict = {
            ImageVariantsTable.c.createdDate.key: createdDate,
            ImageVariantsTable.c.updatedDate.key: updatedDate,
            ImageVariantsTable.c.imageId.key: imageId,
            ImageVariantsTable.c.filename.key: filename,
            ImageVariantsTable.c.isPreview.key: isPreview,
            ImageVariantsTable.c.width.key: width,
            ImageVariantsTable.c.height.key: height,
            ImageVariantsTable.c.area.key: area,
        }
        query = ImageVariantsTable.insert().values(values).returning(ImageVariantsTable.c.imageVariantId)
        result = await self._execute(query=query, connection=connection)
        imageVariantId = str(result.scalar_one())
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
        values: CreateRecordDict = {
            UrlUploadsTable.c.createdDate.key: createdDate,
            UrlUploadsTable.c.updatedDate.key: updatedDate,
            UrlUploadsTable.c.url.key: url,
            UrlUploadsTable.c.imageId.key: imageId,
        }
        query = UrlUploadsTable.insert().values(values).returning(UrlUploadsTable.c.urlUploadId)
        result = await self._execute(query=query, connection=connection)
        urlUploadId = str(result.scalar_one())
        return UrlUpload(
            urlUploadId=urlUploadId,
            createdDate=createdDate,
            updatedDate=updatedDate,
            url=url,
            imageId=imageId,
        )
