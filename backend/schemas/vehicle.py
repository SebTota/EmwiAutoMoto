from typing import Optional, List

from pydantic import BaseModel

from backend.schemas.media import MediaRead
from backend.schemas.product import ProductBase, ProductCreate, ProductList


class VehicleBase(ProductBase):
    year: int
    make: str
    model: str
    vin: Optional[str] = None
    odometer: int
    color: str


class VehicleReadWithMedia(VehicleBase):
    thumbnail_url: str
    medium_thumbnail_url: str
    media: List[MediaRead]


class VehicleReadNoMedia(VehicleBase):
    thumbnail_url: str
    medium_thumbnail_url: str


class VehicleCreate(ProductCreate):
    year: int
    make: str
    model: str
    vin: Optional[str] = None
    odometer: int
    color: str


class VehicleList(ProductList):
    pass


class VehicleAIRecommendation(BaseModel):
    make: str
    model: str
    description: str
