from pydantic import BaseModel
import Motorcycle


class MotorcycleListResponse(BaseModel):
    num_items: int
    items: [Motorcycle]
    next_page_start: int
