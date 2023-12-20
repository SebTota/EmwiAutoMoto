from typing import Optional, List

from sqlmodel import Session

from backend.models import Image
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
    obj_update_data = obj_update.dict(exclude_unset=True)

    # Update the simple attributes of Motorcycle
    for k, v in obj_update_data.items():
        if k != "images":
            setattr(db_obj, k, v)

    # Handle the images relationship separately
    if "images" in obj_update_data:
        updated_image_ids: [str] = [image.id for image in obj_update.images]
        removed_image_ids: [str] = []
        for image in db_obj.images:
            if image.id not in updated_image_ids:
                removed_image_ids.append(image.id)

        print(f'Removing images: {removed_image_ids} for motorcycle id: {db_obj.id}')

        for removed_image_id in removed_image_ids:
            # TODO: Also remove the image from object storage
            db.query(Image).filter(Image.id == removed_image_id).delete()

    # TODO: Update the thumbnail url if the thumbnail image was removed

    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_multi_with_filters(db: Session, offset: int = 0, limit: int = 100,
                           show_status: MotorcycleStatus = MotorcycleStatus.for_sale.value) -> List[Motorcycle]:
    return db.query(Motorcycle) \
        .filter(Motorcycle.status == show_status)\
        .order_by(Motorcycle.date_created)\
        .offset(offset)\
        .limit(limit)\
        .all()
