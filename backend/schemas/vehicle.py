from typing import Optional, List

from backend.schemas.media import MediaRead
from backend.schemas.product import ProductBase, ProductCreate


class VehicleBase(ProductBase):
    year: int
    make: str
    model: str
    vin: Optional[str] = None
    odometer: int
    color: str


class VehicleReadWithMedia(ProductBase):
    thumbnail_url: str
    medium_thumbnail_url: str
    media: List[MediaRead]


class VehicleReadNoMedia(ProductBase):
    thumbnail_url: str
    medium_thumbnail_url: str


class VehicleCreate(ProductCreate):
    year: int
    make: str
    model: str
    vin: Optional[str] = None
    odometer: int

