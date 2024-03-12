import enum

from backend.models.media import Media
from tortoise import fields, models


class ProductStatus(str, enum.Enum):
    DRAFT = "Szkic"
    FOR_SALE = "Na sprzedaż"
    SOLD = "Sprzedany"
    RESERVED = "Zarezerwowany"
    DELETED = "Usunięty"


class Product(models.Model):
    id = fields.CharField(max_length=12, pk=True, index=True)
    date_created = fields.DatetimeField(auto_now_add=True)
    date_last_updated = fields.DatetimeField(auto_now=True)
    price = fields.IntField(null=True)
    description = fields.TextField(null=True)
    status = fields.CharEnumField(ProductStatus)
    thumbnail_url = fields.CharField(max_length=512)
    medium_thumbnail_url = fields.CharField(max_length=512)
    media = fields.ReverseRelation[Media]
