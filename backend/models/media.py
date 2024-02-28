import enum
from typing import TYPE_CHECKING

from tortoise import fields, models

if TYPE_CHECKING:
    from backend.models import Product


class MediaType(str, enum.Enum):
    IMAGE = 'IMAGE'
    YOUTUBE_VIDEO = 'YOUTUBE_VIDEO'


class Media(models.Model):
    id: str = fields.CharField(max_length=20, pk=True)
    type = fields.CharEnumField(MediaType, default=MediaType.IMAGE)
    url: str = fields.CharField(max_length=512)
    thumbnail_url: str = fields.CharField(max_length=512)
    medium_thumbnail_url: str = fields.CharField(max_length=512)
    order: int = fields.IntField()
    product: fields.ForeignKeyRelation["Product"] = fields.ForeignKeyField(
        'models.Product', related_name='media'
    )
