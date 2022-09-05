from datetime import datetime

from pydantic import BaseModel, validator
from typing import List, Union, Any, Optional

from .Image import Image
from .Video import Video
from backend.models.enums import OdometerMeasurementEnum, ProductStatusEnum
from backend.utils.conversions import miles_to_kilometers


class Motorcycle(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        if 'odometer' in data and data['odometer'] is not None \
                and 'odometer_measurement' in data and data['odometer_measurement'] is not None:
            self.__fields_set__.add('km')

    id: Union[str, None]  # Only used for response, ignored in request
    date_created: Union[datetime, None]  # Only used for response, ignored in request
    date_last_updated: Union[datetime, None]  # Only used for response, ignored in request
    year: int
    make: str
    model: str
    odometer: int
    odometer_measurement: OdometerMeasurementEnum
    km: Union[int, None]  # Only used for response, ignored in request
    color: str
    price: int
    description: str
    sold: bool
    status: Union[ProductStatusEnum, None]
    thumbnail: Optional[str]
    images: Optional[List[Image]]
    videos: Optional[List[Video]]

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


class UpdateMotorcycle(BaseModel):
    id: Union[str, None]  # Only used for response, ignored in request
    date_created: Union[datetime, None]  # Only used for response, ignored in request
    date_last_updated: Union[datetime, None]  # Only used for response, ignored in request
    year: Optional[int]
    make: Optional[str]
    model: Optional[str]
    odometer: Optional[int]
    # Can not use validator to ensure this is Optional but not None so set default case instead. Acts similar.
    odometer_measurement: OdometerMeasurementEnum = None
    km: Union[int, None]  # Only used for response, ignored in request
    color: Optional[str]
    price: Optional[int]
    description: Optional[str]
    sold: Optional[bool]
    status: Union[ProductStatusEnum, None]
    thumbnail: Optional[str]
    images: Optional[List[Image]]
    videos: Optional[List[Video]]

    class Config:
        use_enum_values = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if 'odometer' in data and data['odometer'] is not None \
                and 'odometer_measurement' in data and data['odometer_measurement'] is not None:
            self.__fields_set__.add('km')

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

    # The following validators assert that although the values are optional, then may not be None/null
    @validator('year')
    def validator_year(cls, v):
        assert v is not None, 'year may not be None'
        return v

    @validator('make')
    def validator_make(cls, v):
        assert v is not None, 'make may not be None'
        return v

    @validator('model')
    def validator_model(cls, v):
        assert v is not None, 'model may not be None'
        return v

    @validator('odometer')
    def validator_odometer(cls, v):
        assert v is not None, 'odometer may not be None'
        assert v >= 0, 'odometer may not be less than 0'
        return v

    @validator('color')
    def validator_color(cls, v):
        assert v is not None, 'color may not be None'
        return v

    @validator('price')
    def validator_price(cls, v):
        assert v is not None, 'price may not be None'
        assert v >= 0, 'price may not be less than 0'
        return v

    @validator('description')
    def validator_description(cls, v):
        assert v is not None, 'description may not be None'
        return v

    @validator('sold')
    def validator_sold(cls, v):
        assert v is not None, 'sold may not be None'
        return v

    @validator('status')
    def validator_status(cls, v):
        assert v is not None, 'status may not be None'
        return v

    @validator('thumbnail')
    def validator_thumbnail(cls, v):
        assert v is not None, 'thumbnail may not be None'
        return v

    @validator('images')
    def validator_images(cls, v):
        assert v is not None, 'images may not be None'
        return v

    @validator('videos')
    def validator_videos(cls, v):
        assert v is not None, 'videos may not be None'
        return v
