from typing import Optional

from core.store.database import DatabaseConnection
from core.store.saver import Saver as CoreSaver
from core.util import date_util

from pablo.internal.model import Image
from pablo.store.schema import ImagesTable


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
