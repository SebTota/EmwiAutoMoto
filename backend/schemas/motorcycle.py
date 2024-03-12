from backend.schemas.vehicle import VehicleBase, VehicleCreate, VehicleReadNoMedia, VehicleReadWithMedia


class MotorcycleBase(VehicleBase):
    pass


class MotorcycleReadWithMedia(VehicleReadWithMedia):
    pass


class MotorcycleReadNoMedia(VehicleReadNoMedia):
    pass


class MotorcycleCreate(VehicleCreate):
    pass
