from datetime import datetime

from pydantic.main import BaseModel

from backend.models.product import ProductStatus
from backend.schemas.image import ImageRead, ImageCreate


class ProductReadWithImages(BaseModel):
    id: str
    date_created: datetime
    date_last_updated: datetime
    year: int
    make: str
    model: str
    vin: str
    odometer_miles: int
    color: str
    price: int
    description: str
    status: ProductStatus
    thumbnail_url: str
    medium_thumbnail_url: str
    images: list[ImageRead]


class ProductReadNoImages(BaseModel):
    id: str
    date_created: datetime
    date_last_updated: datetime
    year: int
    make: str
    model: str
    vin: str
    odometer_miles: int
    color: str
    price: int
    description: str
    status: ProductStatus
    thumbnail_url: str
    medium_thumbnail_url: str


class ProductCreate(BaseModel):
    year: int
    make: str
    model: str
    vin: str
    odometer_miles: int
    color: str
    price: int
    description: str
    status: ProductStatus
    images: list[ImageCreate]


class ProductList(BaseModel):
    page: int
    has_next_page: bool
    products: list[ProductReadNoImages]
