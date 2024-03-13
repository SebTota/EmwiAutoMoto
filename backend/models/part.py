from backend.models.product import Product

from sqlalchemy import Column, String, ForeignKey


class Part(Product):
    __tablename__ = 'parts'

    id: str = Column(String, ForeignKey('products.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'part',
    }
