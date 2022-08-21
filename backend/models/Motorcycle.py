from fireo.models import Model
from fireo.fields import TextField, NumberField, BooleanField, ListField


class Motorcycle(Model):
    year: int = NumberField()
    make: str = TextField()
    model: str = TextField()
    km: int = NumberField()
    color: str = TextField()
    price: int = NumberField()
    description: str = TextField()
    sold: bool = BooleanField()
    images: [str] = ListField()
    videos: [str] = ListField()
