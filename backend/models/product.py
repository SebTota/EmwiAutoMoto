import enum

from backend.models.media import Media
from tortoise import fields, models


class ProductType(str, enum.Enum):
    MOTOCYKL = 'Motocykl'
    TRAKTOR = 'Traktor'


class ProductStatus(str, enum.Enum):
    DRAFT = 'DRAFT'
    FOR_SALE = 'FOR_SALE'
    SOLD = 'SOLD'
    RESERVED = 'RESERVED'
    DELETED = 'DELETED'


class OdometerType(str, enum.Enum):
    MIL = 'Mil'
    GODZIN = 'Godzin'


class Product(models.Model):
    id = fields.CharField(max_length=12, pk=True, index=True)
    date_created = fields.DatetimeField(auto_now_add=True, index=True)
    date_last_updated = fields.DatetimeField(auto_now=True, index=True)
    type = fields.CharEnumField(ProductType, index=True, default=ProductType.MOTOCYKL)
    year = fields.IntField()
    make = fields.CharField(max_length=100)
    model = fields.CharField(max_length=100)
    vin = fields.CharField(max_length=100, null=True)
    odometer = fields.IntField()
    odometer_type = fields.CharEnumField(OdometerType, defualt=OdometerType.MIL)
    color = fields.CharField(max_length=100)
    price = fields.IntField(null=True)
    description = fields.TextField(null=True)
    status = fields.CharEnumField(ProductStatus, index=True)
    thumbnail_url = fields.CharField(max_length=512)
    medium_thumbnail_url = fields.CharField(max_length=512)
    media = fields.ReverseRelation[Media]
