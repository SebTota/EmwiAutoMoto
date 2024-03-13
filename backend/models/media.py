import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum

from backend.db.init_db import Base


class MediaType(enum.Enum):
    IMAGE = 'IMAGE'
    YOUTUBE_VIDEO = 'YOUTUBE_VIDEO'


class Media(Base):
    __tablename__ = 'media'

    id: int = Column(String, primary_key=True)
    type: MediaType = Column(Enum(MediaType), nullable=False)
    url: str = Column(String, nullable=False)
    thumbnail_url: str = Column(String, nullable=False)
    medium_thumbnail_url: str = Column(String, nullable=False)
    order: int = Column(Integer, nullable=False)

    product_id: str = Column(String, ForeignKey('products.id'))
