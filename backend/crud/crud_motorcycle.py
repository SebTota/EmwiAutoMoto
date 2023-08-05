from typing import Optional, List

from sqlmodel import Session

from backend.models.motorcycle import Motorcycle, MotorcycleCreate, MotorcycleStatus, MotorcycleUpdate
from backend.utils import get_random_alphanumeric_string


def get(db: Session, obj_id: str) -> Optional[Motorcycle]:
    return db.query(Motorcycle).filter(Motorcycle.id == obj_id).first()


def create(db: Session, obj: MotorcycleCreate) -> Motorcycle:
    db_obj: Motorcycle = Motorcycle.from_orm(obj)
    db_obj.id = get_random_alphanumeric_string(12)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Motorcycle, obj_update: MotorcycleUpdate) -> Motorcycle:
    obj_update_data: dict = obj_update.dict(exclude_unset=True)
    for k, v in obj_update_data.items():
        setattr(db_obj, k, v)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_multi_with_filters(db: Session, offset: int = 0, limit: int = 100, show_sold: bool = False,
                           show_status: MotorcycleStatus = MotorcycleStatus.active.value) -> List[Motorcycle]:
    return db.query(Motorcycle)\
        .filter(Motorcycle.sold == show_sold)\
        .filter(Motorcycle.status == show_status)\
        .order_by(Motorcycle.date_created)\
        .offset(offset)\
        .limit(limit)\
        .all()
