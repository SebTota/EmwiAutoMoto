import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.orm import relationship

from backend.db.init_db import Base


class ProductStatus(enum.Enum):
    DRAFT = "Szkic"
    FOR_SALE = "Na sprzedaż"
    SOLD = "Sprzedane"
    RESERVED = "Zarezerwowane"
    DELETED = "Usunięte"


class Product(Base):
    __tablename__ = 'products'

    id: str = Column(String, primary_key=True)
    date_created: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_last_updated: datetime = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    title: str = Column(String, nullable=False)
    subtitle: str = Column(String, nullable=False)
    price: Optional[int] = Column(Integer, nullable=True)
    description: Optional[str] = Column(Text, nullable=True)
    status: ProductStatus = Column(Enum(ProductStatus), nullable=False)
    thumbnail_url: str = Column(String, nullable=False)
    medium_thumbnail_url: str = Column(String, nullable=False)

    media = relationship("Media", backref="product")

    __mapper_args__ = {
        'polymorphic_identity': 'product',
    }
