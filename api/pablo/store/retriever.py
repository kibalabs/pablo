from typing import Sequence
from typing import Optional

from core.store.retriever import FieldFilter
from core.store.retriever import Order
from core.store.retriever import Retriever as CoreRetriever
from core.exceptions import NotFoundException

from pablo.internal.model import Image, UrlUpload
from pablo.internal.model import ImageVariant
from pablo.store.schema import ImagesTable, UrlUploadsTable
from pablo.store.schema import ImageVariantsTable
from pablo.store.schema_conversions import image_from_row, url_upload_from_row
from pablo.store.schema_conversions import image_variant_from_row

class Retriever(CoreRetriever):

    async def list_images(self, fieldFilters: Optional[Sequence[FieldFilter]] = None, orders: Optional[Sequence[Order]] = None, limit: Optional[int] = None) -> Sequence[Image]:
        query = ImagesTable.select()
        if fieldFilters:
            query = self._apply_field_filters(query=query, table=ImagesTable, fieldFilters=fieldFilters)
        if orders:
            query = self._apply_orders(query=query, table=ImagesTable, orders=orders)
        if limit:
            query = query.limit(limit)
        rows = await self.database.fetch_all(query=query)
        images = [image_from_row(row) for row in rows]
        return images

    async def get_image(self, imageId: str) -> Image:
        query = ImagesTable.select(ImagesTable.c.imageId == imageId)
        row = await self.database.fetch_one(query=query)
        if not row:
            raise NotFoundException(message=f'Image {imageId} not found')
        image = image_from_row(row)
        return image

    async def list_image_variants(self, fieldFilters: Optional[Sequence[FieldFilter]] = None, orders: Optional[Sequence[Order]] = None, limit: Optional[int] = None) -> Sequence[ImageVariant]:
        query = ImageVariantsTable.select()
        if fieldFilters:
            query = self._apply_field_filters(query=query, table=ImageVariantsTable, fieldFilters=fieldFilters)
        if orders:
            query = self._apply_orders(query=query, table=ImageVariantsTable, orders=orders)
        if limit:
            query = query.limit(limit)
        rows = await self.database.fetch_all(query=query)
        imageVariants = [image_variant_from_row(row) for row in rows]
        return imageVariants

    async def get_image_variant(self, imageVariantId: str) -> Image:
        query = ImageVariantsTable.select(ImageVariantsTable.c.id == imageVariantId)
        row = await self.database.fetch_one(query=query)
        if not row:
            raise NotFoundException(message=f'ImageVariant {imageVariantId} not found')
        imageVariant = image_variant_from_row(row)
        return imageVariant

    async def list_url_uploads(self, fieldFilters: Optional[Sequence[FieldFilter]] = None, orders: Optional[Sequence[Order]] = None, limit: Optional[int] = None) -> Sequence[UrlUpload]:
        query = UrlUploadsTable.select()
        if fieldFilters:
            query = self._apply_field_filters(query=query, table=UrlUploadsTable, fieldFilters=fieldFilters)
        if orders:
            query = self._apply_orders(query=query, table=UrlUploadsTable, orders=orders)
        if limit:
            query = query.limit(limit)
        rows = await self.database.fetch_all(query=query)
        urlUploads = [url_upload_from_row(row) for row in rows]
        return urlUploads

    async def get_url_upload(self, urlUploadId: str) -> Image:
        query = UrlUploadsTable.select(UrlUploadsTable.c.id == urlUploadId)
        row = await self.database.fetch_one(query=query)
        if not row:
            raise NotFoundException(message=f'UrlUpload {urlUploadId} not found')
        urlUpload = url_upload_from_row(row)
        return urlUpload

    async def get_url_upload_by_url(self, url: str) -> Image:
        query = UrlUploadsTable.select(UrlUploadsTable.c.url == url)
        row = await self.database.fetch_one(query=query)
        if not row:
            raise NotFoundException(message=f'UrlUpload with url {url} not found')
        urlUpload = url_upload_from_row(row)
        return urlUpload
