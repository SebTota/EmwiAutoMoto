from datetime import datetime

from pydantic import BaseModel
from typing import List, Union
from .Image import Image
from .Video import Video
from backend.models.enums import OdometerMeasurementEnum


class Motorcycle(BaseModel):
    id: Union[str, None]
    date_created: Union[datetime, None]
    date_last_updated: Union[datetime, None]
    year: int
    make: str
    model: str
    odometer: int
    odometer_measurement: OdometerMeasurementEnum
    km: Union[int, None]
    color: str
    price: int
    description: str
    sold: bool
    thumbnail: str
    images: Union[List[Image], None]
    videos: Union[List[Video], None]

    class Config:
        use_enum_values = True
