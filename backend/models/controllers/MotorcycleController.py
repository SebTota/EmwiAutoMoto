from typing import List

from fireo.models import Model
from fireo.fields import TextField, NumberField, BooleanField, ListField


class ImageData(Model):
    thumbnail: str = TextField()
    image: str = TextField()


class VideoData(Model):
    thumbnail: str = TextField()
    video: str = TextField()


class MotorcycleController(Model):
    year: int = NumberField(required=True)
    make: str = TextField(required=True)
    model: str = TextField(required=True)
    km: int = NumberField(required=True)
    color: str = TextField(required=True)
    price: int = NumberField(required=True)
    description: str = TextField(required=True)
    sold: bool = BooleanField(required=True)
    thumbnail: str = TextField(required=True)
    images: List[ImageData] = ListField()
    videos: List[VideoData] = ListField()
