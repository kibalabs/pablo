from pydantic import BaseModel


class ApiImage(BaseModel):
    imageId: str
    width: int
    height: int
    format: str
    url: str


class ApiImageVariant(BaseModel):
    imageId: str
    variantId: str
    width: int
    height: int
    format: str
    url: str
