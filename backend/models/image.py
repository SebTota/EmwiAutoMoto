from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from backend.db.base_class import Base

if TYPE_CHECKING:
    from .motorcycle import Motorcycle  # noqa: F401


class Image(Base):
    id = Column(String(12), primary_key=True, index=True)
    image_url = Column(String, index=True)
    thumbnail_url = Column(String)
    medium_thumbnail_url = Column(String)

    motorcycle_id = Column(String, ForeignKey("motorcycle.id"))
    motorcycle = relationship("Motorcycle", back_populates="images")
