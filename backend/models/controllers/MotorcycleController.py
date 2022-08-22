from typing import List

from fireo.models import Model
from fireo.fields import TextField, NumberField, BooleanField, ListField


class MotorcycleController(Model):
    year: int = NumberField(required=True)
    make: str = TextField(required=True)
    model: str = TextField(required=True)
    km: int = NumberField(required=True)
    color: str = TextField(required=True)
    price: int = NumberField(required=True)
    description: str = TextField(required=True)
    sold: bool = BooleanField(required=True)
    images: List[str] = ListField()
    videos: List[str] = ListField()
