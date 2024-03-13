from typing import List

from backend.schemas.vehicle import VehicleBase, VehicleCreate, VehicleReadWithMedia, VehicleReadNoMedia, VehicleList


class MowerBase(VehicleBase):
    pass


class MowerReadWithMedia(VehicleReadWithMedia):
    pass


class MowerReadNoMedia(VehicleReadNoMedia):
    pass


class MowerCreate(VehicleCreate):
    pass


class MowerList(VehicleList):
    page: int
    has_next_page: bool
    products: List[MowerReadNoMedia]
