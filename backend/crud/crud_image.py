from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.image import Image
from backend.schemas.image import ImageCreate, ImageUpdate
from backend.utils.deps import get_random_string


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    def create(self, db: Session, *, obj_in: ImageCreate) -> Image:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, id=get_random_string(12))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_and_add_to_motorcycle(
            self, db: Session, *, db_obj: Any, obj_in: ImageCreate
    ) -> Image:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, id=get_random_string(12), motorcycle_id=db_obj.id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: Image, obj_in: Union[ImageUpdate, Dict[str, Any]]
    ) -> Image:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


image = CRUDImage(Image)
