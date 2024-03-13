from backend.models import Product

from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vehicle(Product):
    __tablename__ = 'vehicles'

    id: str = Column(String, ForeignKey('products.id'), primary_key=True)
    year: int = Column(Integer, nullable=False)
    make: str = Column(String, nullable=False)
    model: str = Column(String, nullable=False)
    vin: Optional[str] = Column(String, nullable=True)
    odometer: int = Column(Integer, nullable=False)
    color: str = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'vehicle',
    }
