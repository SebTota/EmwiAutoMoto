from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship

from backend.db.base_class import Base

if TYPE_CHECKING:
    from .refresh_token import RefreshToken  # noqa: F401


class User(Base):
    id = Column(String, primary_key=True, index=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    username = Column(String(20), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    refresh_token = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    refresh_token_expires = Column(DateTime)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
