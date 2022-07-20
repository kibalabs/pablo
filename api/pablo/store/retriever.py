from typing import Optional
from typing import Sequence

from core.exceptions import NotFoundException
from core.store.database import DatabaseConnection
from core.store.retriever import FieldFilter
from core.store.retriever import Order
from core.store.retriever import Retriever as CoreRetriever

from pablo.internal.model import Image
from pablo.internal.model import ImageVariant
from pablo.internal.model import UrlUpload
from pablo.store.schema import ImagesTable
from pablo.store.schema import ImageVariantsTable
from pablo.store.schema import UrlUploadsTable
from pablo.store.schema_conversions import image_from_row
from pablo.store.schema_conversions import image_variant_from_row
from pablo.store.schema_conversions import url_upload_from_row


class Retriever(CoreRetriever):

    async def list_images(self, fieldFilters: Optional[Sequence[FieldFilter]] = None, orders: Optional[Sequence[Order]] = None, limit: Optional[int] = None, connection: Optional[DatabaseConnection] = None) -> Sequence[Image]:
        query = ImagesTable.select()
        if fieldFilters:
            query = self._apply_field_filters(query=query, table=ImagesTable, fieldFilters=fieldFilters)
        if orders:
            query = self._apply_orders(query=query, table=ImagesTable, orders=orders)
        if limit:
            query = query.limit(limit)
        result = await self.database.execute(query=query, connection=connection)
        images = [image_from_row(row) for row in result]
        return images

    async def get_image(self, imageId: str, connection: Optional[DatabaseConnection] = None) -> Image:
        query = ImagesTable.select(ImagesTable.c.imageId == imageId)
        result = await self.database.execute(query=query, connection=connection)
        row = result.first()
        if not row:
            raise NotFoundException(message=f'Image {imageId} not found')
        image = image_from_row(row)
        return image

    async def list_image_variants(self, fieldFilters: Optional[Sequence[FieldFilter]] = None, orders: Optional[Sequence[Order]] = None, limit: Optional[int] = None, connection: Optional[DatabaseConnection] = None) -> Sequence[ImageVariant]:
        query = ImageVariantsTable.select()
        if fieldFilters:
            query = self._apply_field_filters(query=query, table=ImageVariantsTable, fieldFilters=fieldFilters)
        if orders:
            query = self._apply_orders(query=query, table=ImageVariantsTable, orders=orders)
        if limit:
            query = query.limit(limit)
        result = await self.database.execute(query=query, connection=connection)
        imageVariants = [image_variant_from_row(row) for row in result]
        return imageVariants

    async def get_image_variant(self, imageVariantId: str, connection: Optional[DatabaseConnection] = None) -> Image:
        query = ImageVariantsTable.select(ImageVariantsTable.c.id == imageVariantId)
        result = await self.database.execute(query=query, connection=connection)
        row = result.first()
        if not row:
            raise NotFoundException(message=f'ImageVariant {imageVariantId} not found')
        imageVariant = image_variant_from_row(row)
        return imageVariant

    async def list_url_uploads(self, fieldFilters: Optional[Sequence[FieldFilter]] = None, orders: Optional[Sequence[Order]] = None, limit: Optional[int] = None, connection: Optional[DatabaseConnection] = None) -> Sequence[UrlUpload]:
        query = UrlUploadsTable.select()
        if fieldFilters:
            query = self._apply_field_filters(query=query, table=UrlUploadsTable, fieldFilters=fieldFilters)
        if orders:
            query = self._apply_orders(query=query, table=UrlUploadsTable, orders=orders)
        if limit:
            query = query.limit(limit)
        result = await self.database.execute(query=query, connection=connection)
        urlUploads = [url_upload_from_row(row) for row in result]
        return urlUploads

    async def get_url_upload(self, urlUploadId: str, connection: Optional[DatabaseConnection] = None) -> Image:
        query = UrlUploadsTable.select(UrlUploadsTable.c.id == urlUploadId)
        result = await self.database.execute(query=query, connection=connection)
        row = result.first()
        if not row:
            raise NotFoundException(message=f'UrlUpload {urlUploadId} not found')
        urlUpload = url_upload_from_row(row)
        return urlUpload

    async def get_url_upload_by_url(self, url: str, connection: Optional[DatabaseConnection] = None) -> Image:
        query = UrlUploadsTable.select(UrlUploadsTable.c.url == url)
        result = await self.database.execute(query=query, connection=connection)
        row = result.first()
        if not row:
            raise NotFoundException(message=f'UrlUpload with url {url} not found')
        urlUpload = url_upload_from_row(row)
        return urlUpload
