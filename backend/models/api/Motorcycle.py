from pydantic import BaseModel
from typing import List, Union
from .Image import Image
from .Video import Video


class Motorcycle(BaseModel):
    id: Union[str, None]
    year: int
    make: str
    model: str
    km: int
    color: str
    price: int
    description: str
    sold: bool
    thumbnail: str
    images: Union[List[Image], None]
    videos: Union[List[Video], None]
