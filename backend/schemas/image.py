from typing import Optional, List

from pydantic import BaseModel

from backend.enums import OdometerMeasurementEnum, ProductStatusEnum


# Shared properties
class ImageBase(BaseModel):
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


# Properties to receive on item creation
class ImageCreate(ImageBase):
    image_url: str
    thumbnail_url: str


# Properties to receive on item update
class ImageUpdate(ImageBase):
    pass


# Properties shared by models stored in DB
class ImageInDBBase(ImageBase):
    id: int
    motorcycle_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Image(ImageInDBBase):
    pass


# Properties stored in DB
class ImageInDB(ImageInDBBase):
    pass
