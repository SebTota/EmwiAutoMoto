from typing import Any, Dict, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend import schemas
from backend.crud.base import CRUDBase
from backend.enums import ProductStatusEnum
from backend.models.motorcycle import Motorcycle
from backend.schemas.motorcycle import MotorcycleCreate, MotorcycleUpdate
from backend.utils.deps import get_random_string


class CRUDMotorcycle(CRUDBase[Motorcycle, MotorcycleCreate, MotorcycleUpdate]):

    def create(self, db: Session, *, obj_in: MotorcycleCreate) -> Motorcycle:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, id=get_random_string(12))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: Motorcycle, obj_in: Union[MotorcycleUpdate, Dict[str, Any]]
    ) -> Motorcycle:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    page: int
    has_next_page: bool
    total_items: int
    motorcycles: List[Motorcycle]
    motorcycle_count: int

    def get_multi_with_filters(
        self, db: Session, *, page: int, limit: int, show_sold: bool, show_status: ProductStatusEnum
    ) -> schemas.MotorcycleList:
        offset: int = (page - 1) * limit

        q = db.query(self.model) \
            .where(Motorcycle.sold == show_sold) \
            .where(Motorcycle.status == show_status) \
            .order_by(desc(Motorcycle.date_created))
        total_count: int = q.count()
        motorcycles: List[schemas.Motorcycle] = q.offset(offset).limit(limit + 1).all()

        if not motorcycles:
            return schemas.MotorcycleList(page=page,
                                          has_next_page=False,
                                          total_count=total_count,
                                          motorcycles=[],
                                          count=0)

        has_next_page = True if len(motorcycles) == limit + 1 else False

        # Remove the extra motorcycle we got as a pagination test IFF there is a next page
        # (indicating we received +1 results back from db)
        if has_next_page:
            motorcycles.pop()

        return schemas.MotorcycleList(page=page,
                                      has_next_page=has_next_page,
                                      total_count=total_count,
                                      motorcycles=motorcycles,
                                      count=len(motorcycles))


motorcycle = CRUDMotorcycle(Motorcycle)
