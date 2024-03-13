from backend.models.vehicle import Vehicle

from sqlalchemy import Column, String, ForeignKey


class Mower(Vehicle):
    __tablename__ = 'mowers'

    id: str = Column(String, ForeignKey('vehicles.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'mower',
    }
