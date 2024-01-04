from typing import TYPE_CHECKING

from tortoise import fields, models

if TYPE_CHECKING:
    from backend.models import Product


class Image(models.Model):
    id: str = fields.CharField(max_length=20, pk=True)
    image_url: str = fields.CharField(max_length=512)
    thumbnail_url: str = fields.CharField(max_length=512)
    medium_thumbnail_url: str = fields.CharField(max_length=512)
    order: int = fields.IntField()
    product: fields.ForeignKeyRelation["Product"] = fields.ForeignKeyField(
        'models.Product', related_name='images'
    )
