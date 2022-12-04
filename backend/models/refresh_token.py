from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from backend.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class RefreshToken(Base):
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.id"))
    user = relationship("User", back_populates="refresh_token")
    refresh_token = Column(String(210), index=True)
    expires = Column(DateTime)
