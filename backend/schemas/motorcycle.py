from typing import List

from backend.schemas.vehicle import VehicleBase, VehicleCreate, VehicleReadNoMedia, VehicleReadWithMedia, VehicleList


class MotorcycleBase(VehicleBase):
    pass


class MotorcycleReadWithMedia(VehicleReadWithMedia):
    pass


class MotorcycleReadNoMedia(VehicleReadNoMedia):
    pass


class MotorcycleCreate(VehicleCreate):
    pass


class MotorcycleList(VehicleList):
    page: int
    has_next_page: bool
    products: List[MotorcycleReadNoMedia]
