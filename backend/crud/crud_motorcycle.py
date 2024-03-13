from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.models import Media, Motorcycle, ProductStatus, MediaType
from backend.schemas import MediaRead, MotorcycleReadWithMedia, MotorcycleReadNoMedia, MediaCreate, MotorcycleCreate
from backend.utils import get_random_alphanumeric_string


def get(db: Session, obj_id: str) -> Optional[Motorcycle]:
    return db.query(Motorcycle).filter(Motorcycle.id == obj_id).first()


def get_with_media(db: Session, obj_id: str) -> Optional[MotorcycleReadWithMedia]:
    motorcycle: Optional[Motorcycle] = db.query(Motorcycle).filter(Motorcycle.id == obj_id).first()

    if not motorcycle:
        return None

    # Preload and sort the Media
    db_media = db.query(Media).filter(Media.product_id == motorcycle.id).order_by(Media.order).all()
    media: [MediaRead] = [MediaRead(id=media_obj.id,
                                    type=media_obj.type,
                                    url=media_obj.url,
                                    thumbnail_url=media_obj.thumbnail_url,
                                    medium_thumbnail_url=media_obj.medium_thumbnail_url,
                                    order=media_obj.order)
                          for media_obj in db_media]

    return MotorcycleReadWithMedia(**motorcycle.__dict__,
                                   media=media)


def create(db: Session, motorcycle_create: MotorcycleCreate) -> Optional[Motorcycle]:
    # Generate thumbnail url, which is the first image's thumbnail url
    thumbnail_url = medium_thumbnail_url = ''
    for media_obj in motorcycle_create.media:
        if media_obj.type == MediaType.IMAGE:
            thumbnail_url, medium_thumbnail_url = media_obj.thumbnail_url, media_obj.medium_thumbnail_url

    # Create the motorcycle object
    motorcycle = Motorcycle(id=get_random_alphanumeric_string(12),
                            thumbnail_url=thumbnail_url,
                            medium_thumbnail_url=medium_thumbnail_url,
                            **motorcycle_create.dict(exclude={"media", "thumbnail_url"}))

    db.add(motorcycle)
    db.commit()
    db.refresh(motorcycle)

    # Create the nested Media objects
    if motorcycle_create.media:
        i, media_objs = 0, []
        for media_obj in motorcycle_create.media:
            media_obj: MediaCreate = media_obj  # Add type support
            media_objs.append(Media(product_id=motorcycle.id,
                                    id=get_random_alphanumeric_string(20),
                                    type=media_obj.type,
                                    url=media_obj.url,
                                    thumbnail_url=media_obj.thumbnail_url,
                                    medium_thumbnail_url=media_obj.medium_thumbnail_url,
                                    order=i))

        db.bulk_save_objects(media_objs)
        db.commit()

    return get(db, motorcycle.id)


def update(db: Session, db_obj: Motorcycle, new_obj: MotorcycleCreate) -> Optional[MotorcycleReadWithMedia]:
    # Update the Motorcycle attributes
    update_dict: dict = new_obj.dict(exclude={"media", "thumbnail_url", "medium_thumbnail_url"})
    update_dict['thumbnail_url'] = new_obj.media[0].thumbnail_url if new_obj.media else ''
    update_dict['medium_thumbnail_url'] = new_obj.media[0].medium_thumbnail_url if new_obj.media else ''

    for key, value in update_dict.items():
        setattr(db_obj, key, value)

    db.commit()
    db.refresh(db_obj)

    for media_obj in db_obj.media:
        # TODO: Make sure we remove any actually deleted items from object storage
        db.delete(media_obj)

    if new_obj.media:
        i, media_objs = 0, []
        for media_obj in new_obj.media:
            media_obj: MediaCreate = media_obj  # Add type support
            media_objs.append(Media(product_id=db_obj.id,
                                    id=get_random_alphanumeric_string(20),
                                    type=media_obj.type,
                                    url=media_obj.url,
                                    thumbnail_url=media_obj.thumbnail_url,
                                    medium_thumbnail_url=media_obj.medium_thumbnail_url,
                                    order=i))
            i += 1

        db.bulk_save_objects(media_objs)
        db.commit()

    return get(db, db_obj.id)


def get_multi_with_filters(db: Session, offset: int, limit: int, show_status: [ProductStatus]) -> List[
    MotorcycleReadNoMedia]:
    motorcycles: List[Motorcycle] = (db.query(Motorcycle)
                                     .filter(Motorcycle.status.in_(show_status))
                                     .order_by(desc(Motorcycle.date_created))
                                     .offset(offset)
                                     .limit(limit)
                                     .all())
    return [MotorcycleReadNoMedia(**m.__dict__) for m in motorcycles]
