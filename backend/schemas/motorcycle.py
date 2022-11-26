from typing import Optional, List, Any

from pydantic import BaseModel
from pydantic.class_validators import validator

from .image import Image
from backend.enums import OdometerMeasurementEnum, ProductStatusEnum


# Shared properties
from backend.utils.conversions import miles_to_kilometers


class MotorcycleBase(BaseModel):
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[int] = None
    odometer_measurement: Optional[OdometerMeasurementEnum] = None
    km: int = None  # This value is set using odometer and odometer_measurement, NOT passed in as a variable
    color: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    sold: Optional[bool] = None
    status: Optional[ProductStatusEnum] = None
    thumbnail: Optional[str] = None
    images: Optional[List[Image]] = []

    class Config:
        use_enum_values = True

    @validator('km', pre=True, always=True)
    def set_km_value(cls, v, values):
        if 'odometer' in values and values['odometer'] is not None \
                and 'odometer_measurement' in values and values['odometer_measurement'] is not None:
            if values['odometer_measurement'] == OdometerMeasurementEnum.km.value:
                return values['odometer']
            elif values['odometer_measurement'] == OdometerMeasurementEnum.mi.value:
                return miles_to_kilometers(values['odometer'])

    @validator('odometer_measurement', always=True)
    def odometer_measurement_validation(cls, v, values, **kwargs):
        """
        If odometer is provided, so much odometer_measurement. Likewise, if odometer_measurement is provided
        so must odometer.
        """
        if v is not None:
            assert 'odometer' in values and values['odometer'] is not None, \
                'odometer value must be provided when updating the odometer_measurement.'

        if v is None:
            assert 'odometer' not in values or values['odometer'] is None, \
                'odometer_measurement must be provided when updating the odometer value.'

        return v


# Properties to receive on motorcycle creation
class MotorcycleCreate(MotorcycleBase):
    year: int
    make: str
    model: str
    odometer: int
    odometer_measurement: OdometerMeasurementEnum
    color: str
    price: int
    description: str
    sold: bool
    status: ProductStatusEnum


# Properties to receive on item update
class MotorcycleUpdate(MotorcycleBase):
    pass


# Properties shared by models stored in DB
class MotorcycleInDBBase(MotorcycleBase):
    id: str
    date_created: Any
    date_last_updated: Any

    class Config:
        orm_mode = True


# Properties to return to client
class Motorcycle(MotorcycleInDBBase):
    pass


# Properties stored in DB
class MotorcycleInDB(MotorcycleInDBBase):
    pass


# Used for pagination
class MotorcycleList(BaseModel):
    cursor: Optional[int]  # If None, that means we are on the last page
    has_next_page: bool
    motorcycles: List[Motorcycle]
