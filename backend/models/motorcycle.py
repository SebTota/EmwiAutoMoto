from backend.models.vehicle import Vehicle

from sqlalchemy import Column, String, ForeignKey


class Motorcycle(Vehicle):
    __tablename__ = 'motorcycles'

    id: str = Column(String, ForeignKey('vehicles.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'motorcycle',
    }
