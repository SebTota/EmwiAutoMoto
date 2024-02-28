from pydantic.main import BaseModel

from backend.models.media import MediaType


class MediaRead(BaseModel):
    type: MediaType
    url: str
    thumbnail_url: str
    medium_thumbnail_url: str


class MediaCreate(BaseModel):
    type: MediaType
    url: str
    thumbnail_url: str
    medium_thumbnail_url: str
