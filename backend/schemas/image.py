from typing import Optional, List

from pydantic import BaseModel


# Shared properties
class ImageBase(BaseModel):
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    medium_thumbnail_url: Optional[str] = None


# Properties to receive on item creation
class ImageCreate(ImageBase):
    image_url: str
    thumbnail_url: str
    medium_thumbnail_url = str


# Properties to receive on item update
class ImageUpdate(ImageBase):
    pass


# Properties shared by models stored in DB
class ImageInDBBase(ImageBase):
    id: str

    class Config:
        orm_mode = True


# Properties to return to client
class Image(ImageInDBBase):
    pass


# Properties stored in DB
class ImageInDB(ImageInDBBase):
    motorcycle_id: str
