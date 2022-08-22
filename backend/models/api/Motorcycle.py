from pydantic import BaseModel
from typing import List, Union


class Motorcycle(BaseModel):
    key: Union[str, None]
    year: int
    make: str
    model: str
    km: int
    color: str
    price: int
    description: str
    sold: bool
    images: Union[List[str], None]
    videos: Union[List[str], None]
