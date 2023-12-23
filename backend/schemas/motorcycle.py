from datetime import datetime

from pydantic.main import BaseModel

from backend.models.motorcycle import MotorcycleStatus
from backend.schemas.image import ImageRead, ImageCreate


class MotorcycleReadWithImages(BaseModel):
    id: str
    date_created: datetime
    date_last_updated: datetime
    year: int
    make: str
    model: str
    odometer_miles: int
    color: str
    price: int
    description: str
    status: MotorcycleStatus
    thumbnail_url: str
    medium_thumbnail_url: str
    images: list[ImageRead]


class MotorcycleReadNoImages(BaseModel):
    id: str
    date_created: datetime
    date_last_updated: datetime
    year: int
    make: str
    model: str
    odometer_miles: int
    color: str
    price: int
    description: str
    status: MotorcycleStatus
    thumbnail_url: str
    medium_thumbnail_url: str


class MotorcycleCreate(BaseModel):
    year: int
    make: str
    model: str
    odometer_miles: int
    color: str
    price: int
    description: str
    status: MotorcycleStatus
    images: list[ImageCreate]


class MotorcycleList(BaseModel):
    page: int
    has_next_page: bool
    motorcycles: list[MotorcycleReadNoImages]
