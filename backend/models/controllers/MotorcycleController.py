from typing import List

from fireo.models import Model
from fireo.fields import TextField, NumberField, BooleanField, ListField


class MotorcycleController(Model):
    year: int = NumberField()
    make: str = TextField()
    model: str = TextField()
    km: int = NumberField()
    color: str = TextField()
    price: int = NumberField()
    description: str = TextField()
    sold: bool = BooleanField()
    images: List[str] = ListField()
    videos: List[str] = ListField()
