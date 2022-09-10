from typing import List, Union
from pydantic import BaseModel

from backend.models.schemas import Motorcycle


class MotorcycleListResponse(BaseModel):
    num_items: int
    items: List[Motorcycle]
    page: int
    has_next_page: bool
