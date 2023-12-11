from typing import Optional

from sqlmodel import Session

from backend.models.image import Image, ImageCreate
from backend.utils import get_random_alphanumeric_string


def get(db: Session, obj_id: str) -> Optional[Image]:
    return db.query(Image).filter(Image.id == obj_id).first()


def create(db: Session, obj: ImageCreate) -> Image:
    db_obj: Image = Image.from_orm(obj)
    db_obj.id = get_random_alphanumeric_string(12)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
