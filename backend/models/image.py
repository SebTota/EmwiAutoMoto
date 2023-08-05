from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .motorcycle import Motorcycle  # noqa: F401


class ImageBase(SQLModel):
    image_url: str = Field(index=True, nullable=False)
    thumbnail_url: str = Field(index=True, nullable=False)
    motorcycle_id: str = Field(foreign_key="motorcycle.id", nullable=False)
    motorcycle: "Motorcycle" = Relationship(back_populates="images")


class Image(ImageBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True, index=True)


class ImageCreate(ImageBase):
    pass


class ImageRead(SQLModel):
    id: str
    image_url: str
    thumbnail_url: str
