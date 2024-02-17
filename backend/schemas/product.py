from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from backend.models.product import ProductStatus, ProductType, OdometerType
from backend.schemas.image import ImageRead, ImageCreate


class ProductBase(BaseModel):
    id: str
    date_created: datetime
    date_last_updated: datetime
    type: ProductType
    year: int
    make: str
    model: str
    vin: Optional[str] = None
    odometer: int
    odometer_type: OdometerType
    color: str
    price: Optional[int] = None
    description: Optional[str] = None
    status: ProductStatus


class ProductReadWithImages(ProductBase):
    thumbnail_url: str
    medium_thumbnail_url: str
    images: List[ImageRead]


class ProductReadNoImages(ProductBase):
    thumbnail_url: str
    medium_thumbnail_url: str


class ProductCreate(BaseModel):
    type: ProductType
    year: int
    make: str
    model: str
    vin: Optional[str] = None
    odometer: int
    odometer_type: OdometerType
    color: str
    price: Optional[int] = None
    description: Optional[str] = None
    status: ProductStatus
    images: List[ImageCreate]


class ProductList(BaseModel):
    page: int
    has_next_page: bool
    products: List[ProductReadNoImages]
