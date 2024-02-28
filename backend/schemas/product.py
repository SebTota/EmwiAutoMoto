from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from backend.models.product import ProductStatus, ProductType, OdometerType
from backend.schemas.media import MediaRead, MediaCreate


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


class ProductReadWithMedia(ProductBase):
    thumbnail_url: str
    medium_thumbnail_url: str
    media: List[MediaRead]


class ProductReadNoMedia(ProductBase):
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
    media: List[MediaCreate]


class ProductList(BaseModel):
    page: int
    has_next_page: bool
    products: List[ProductReadNoMedia]
