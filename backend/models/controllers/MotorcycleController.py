from datetime import datetime
from typing import List

from fireo.models import Model
from fireo.fields import TextField, NumberField, BooleanField, ListField, DateTime

from backend.models.api.Motorcycle import Motorcycle

EXCLUDE_KEYS_FROM_DB_TO_MODEL_MAP = {'key', 'id'}


class ImageData(Model):
    thumbnail: str = TextField()
    image: str = TextField()


class VideoData(Model):
    thumbnail: str = TextField()
    video: str = TextField()


class MotorcycleController(Model):
    date_created: datetime = DateTime()
    date_last_updated: datetime = DateTime()
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

    @staticmethod
    def update_motorcycle(motorcycle: Motorcycle) -> None:
        motorcycle.date_last_updated = datetime.utcnow()
        m: MotorcycleController = MotorcycleController.from_dict(
            motorcycle.dict(exclude=EXCLUDE_KEYS_FROM_DB_TO_MODEL_MAP))

        m._field_changed.remove('date_created')  # Do not update/remove the date_created field
        m.update(f'motorcycle_controller/{motorcycle.id}')

    @staticmethod
    def add_motorcycle(motorcycle: Motorcycle) -> None:
        motorcycle.date_created = datetime.utcnow()
        motorcycle.date_last_updated = datetime.utcnow()
        m: MotorcycleController = MotorcycleController.from_dict(
            motorcycle.dict(exclude=EXCLUDE_KEYS_FROM_DB_TO_MODEL_MAP))
        m.save()
