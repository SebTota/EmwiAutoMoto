from pydantic.main import BaseModel


class ImageRead(BaseModel):
    id: str
    image_url: str
    thumbnail_url: str
    medium_thumbnail_url: str


class ImageCreate(BaseModel):
    image_url: str
    thumbnail_url: str
    medium_thumbnail_url: str
