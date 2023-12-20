import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, condecimal

from .image import Image
if TYPE_CHECKING:
    from .image import Image  # noqa: F401


class MotorcycleStatus(str, enum.Enum):
    draft = 'draft'
    for_sale = 'for_sale'
    sold = 'sold'
    deleted = 'deleted'


class MotorcycleBase(SQLModel):
    date_created: datetime = Field(default=datetime.utcnow(), nullable=False)
    date_last_updated: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    year: int = Field(nullable=False)
    make: str = Field(nullable=False)
    model: str = Field(nullable=False)
    odometer_miles: int = Field(nullable=False)
    color: str = Field(nullable=False)
    price: int = Field(nullable=False)
    description: str = Field(nullable=False)
    status: MotorcycleStatus = Field(index=True, nullable=False)
    thumbnail_url: str = Field(nullable=False)
    images: List["Image"] = Relationship(back_populates="motorcycle")


class Motorcycle(MotorcycleBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True, index=True)
    images: List["Image"] = Relationship(back_populates="motorcycle")


class MotorcycleCreate(MotorcycleBase):
    pass


class MotorcycleRead(MotorcycleBase):
    id: str
    images: List[Image]


class MotorcycleUpdate(SQLModel):
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    odometer_miles: Optional[int] = None
    color: Optional[str] = None
    price: Optional[condecimal(decimal_places=2)] = None
    description: Optional[str] = None
    status: Optional[MotorcycleStatus] = None
    thumbnail_url: Optional[str] = None
    images: Optional[List["Image"]] = None


class MotorcycleList(BaseModel):
    page: int
    has_next_page: bool
    motorcycles: List[MotorcycleRead]
