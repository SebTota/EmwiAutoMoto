import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, condecimal

if TYPE_CHECKING:
    from .image import Image  # noqa: F401


class OdometerMeasurement(str, enum.Enum):
    km = 'km'
    mi = 'mi'


class MotorcycleStatus(str, enum.Enum):
    draft = 'draft'
    active = 'active'
    deleted = 'deleted'


class MotorcycleBase(SQLModel):
    date_created: datetime = Field(default=datetime.utcnow(), nullable=False)
    date_last_updated: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    year: int = Field(index=True, nullable=False)
    make: str = Field(index=True, nullable=False)
    model: str = Field(index=True, nullable=False)

    odometer: int = Field(nullable=False)
    odometer_measurement: OdometerMeasurement = Field(nullable=False)
    km: int = Field(index=True, nullable=False)

    color: str = Field(index=True, nullable=False)
    price: condecimal(decimal_places=2) = Field(index=True, nullable=False)
    description: str = Field(nullable=False)
    sold: bool = Field(index=True, nullable=False)
    status: MotorcycleStatus = Field(index=True, nullable=False)

    thumbnail_url: str = Field(nullable=False)
    images: List["Image"] = Relationship(back_populates="motorcycle")


class Motorcycle(MotorcycleBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)


class MotorcycleCreate(MotorcycleBase):
    pass


class MotorcycleRead(MotorcycleBase):
    id: str


class MotorcycleUpdate(SQLModel):
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[int] = None
    odometer_measurement: Optional[OdometerMeasurement] = None
    km: Optional[int] = None
    color: Optional[str] = None
    price: Optional[condecimal(decimal_places=2)] = None
    description: Optional[str] = None
    sold: Optional[bool] = None
    status: Optional[MotorcycleStatus] = None
    thumbnail_url: Optional[str] = None


class MotorcycleList(BaseModel):
    page: int
    has_next_page: bool
    total_count: int
    motorcycles: List[MotorcycleRead]
    count: int
