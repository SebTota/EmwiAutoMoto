from backend.schemas.vehicle import VehicleBase, VehicleCreate, VehicleReadWithMedia, VehicleReadNoMedia


class MowerBase(VehicleBase):
    pass


class MowerReadWithMedia(VehicleReadWithMedia):
    pass


class MowerReadNoMedia(VehicleReadNoMedia):
    pass


class MowerCreate(VehicleCreate):
    pass
