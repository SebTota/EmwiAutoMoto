from datetime import datetime
from typing import List, Set

from fireo.models import Model
from fireo.fields import TextField, NumberField, BooleanField, ListField, DateTime

from backend.models.api import Image
from backend.models.api.Motorcycle import Motorcycle, UpdateMotorcycle
from backend.utils.image_handler import delete_image

EXCLUDE_KEYS_FROM_DB_TO_MODEL_MAP_FOR_NEW = {'key', 'id'}
EXCLUDE_KEYS_FROM_DB_TO_MODEL_MAP_FOR_UPDATE = {'key', 'id', 'date_created'}


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
    odometer: int = NumberField(required=True)
    odometer_measurement: str = TextField(required=True)
    km: int = NumberField(required=True)
    color: str = TextField(required=True)
    price: int = NumberField(required=True)
    description: str = TextField(required=True)
    sold: bool = BooleanField(required=True)
    thumbnail: str = TextField(required=True)
    images: List[ImageData] = ListField()
    videos: List[VideoData] = ListField()

    @staticmethod
    def update_motorcycle(id: str, motorcycle: UpdateMotorcycle, update_keys: Set[str]) -> Model:
        old_motorcycle: Motorcycle = MotorcycleController.collection.get(f'motorcycle_controller/{id}')
        if old_motorcycle is None:
            raise Exception('Invalid motorcycle id')

        if motorcycle.images is not None:
            new_images: List[Image] = motorcycle.images
            old_images: List[Image] = old_motorcycle.images
            removed_images: List[Image] = [image for image in old_images if image not in new_images]
            print(f'Removing images: ${removed_images}')
            for image in removed_images:
                delete_image(image)

        motorcycle.date_last_updated = datetime.utcnow()
        m: MotorcycleController = MotorcycleController.from_dict(
            motorcycle.dict(exclude=EXCLUDE_KEYS_FROM_DB_TO_MODEL_MAP_FOR_UPDATE, include=update_keys))

        return m.update(f'motorcycle_controller/{id}')

    @staticmethod
    def add_motorcycle(motorcycle: Motorcycle) -> Model:
        motorcycle.date_created = datetime.utcnow()
        motorcycle.date_last_updated = datetime.utcnow()

        m: MotorcycleController = MotorcycleController.from_dict(
            motorcycle.dict(exclude=EXCLUDE_KEYS_FROM_DB_TO_MODEL_MAP_FOR_NEW))
        return m.save()
