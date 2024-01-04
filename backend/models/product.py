import enum

from backend.models.image import Image

from tortoise import fields, models


class ProductStatus(str, enum.Enum):
    DRAFT = 'DRAFT'
    FOR_SALE = 'FOR_SALE'
    SOLD = 'SOLD'
    RESERVED = 'RESERVED'
    DELETED = 'DELETED'


class Product(models.Model):
    id = fields.CharField(max_length=12, pk=True, index=True)
    date_created = fields.DatetimeField(auto_now_add=True, index=True)
    date_last_updated = fields.DatetimeField(auto_now=True, index=True)
    year = fields.IntField()
    make = fields.CharField(max_length=100)
    model = fields.CharField(max_length=100)
    vin = fields.CharField(max_length=100)
    odometer_miles = fields.IntField()
    color = fields.CharField(max_length=100)
    price = fields.IntField()
    description = fields.TextField()
    status = fields.CharEnumField(ProductStatus, index=True)
    thumbnail_url = fields.CharField(max_length=512)
    medium_thumbnail_url = fields.CharField(max_length=512)
    images = fields.ReverseRelation[Image]

