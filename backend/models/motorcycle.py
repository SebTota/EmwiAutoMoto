from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Boolean, func, DateTime
from sqlalchemy.orm import relationship

from backend.db.base_class import Base

if TYPE_CHECKING:
    from .image import Image  # noqa: F401


class Motorcycle(Base):
    id = Column(String(12), primary_key=True, index=True)
    date_created = Column(DateTime, server_default=func.now(), index=True)
    date_last_updated = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp(), index=True)
    year = Column(Integer)
    make = Column(String(50))
    model = Column(String(50))

    # Odometer and odometer measurement is used in UI to display km and miles, but km is used for sorting
    odometer = Column(Integer)
    odometer_measurement = Column(String(5))
    km = Column(Integer)

    color = Column(String(20))
    price = Column(Integer)
    description = Column(String)
    sold = Column(Boolean(), index=True)
    status = Column(String(10), index=True)

    # Store a copy of the current thumbnail to prevent a need to get all images
    thumbnail_url = Column(String)
    images = relationship("Image", back_populates="motorcycle", cascade="all, delete-orphan")
