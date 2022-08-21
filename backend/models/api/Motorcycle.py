from pydantic import BaseModel
from typing import List


class Motorcycle(BaseModel):
    year: int
    make: str
    model: str
    km: int
    color: str
    price: int
    description: str
    sold: bool
    images: List[str]
    videos: List[str]
