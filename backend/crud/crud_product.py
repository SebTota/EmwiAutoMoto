from abc import ABC
from typing import Optional, List
from sqlalchemy import desc
from sqlalchemy.orm import Session

from backend.models import Media, Product, ProductStatus, MediaType
from backend.schemas import MediaRead, ProductReadWithMedia, ProductReadNoMedia, MediaCreate, ProductCreate
from backend.utils import get_random_alphanumeric_string


class AbstractCRUDProduct(ABC):
    model = Product
    schema_create = ProductCreate
    schema_read_with_media = ProductReadWithMedia
    schema_read_no_media = ProductReadNoMedia

    def get(self, db: Session, obj_id: str) -> Optional[model]:
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def get_with_media(self, db: Session, obj_id: str) -> Optional[schema_read_with_media]:
        product: Optional[AbstractCRUDProduct.model] = db.query(self.model).filter(self.model.id == obj_id).first()

        if not product:
            return None

        # Preload and sort the Media
        db_media = db.query(Media).filter(Media.product_id == product.id).order_by(Media.order).all()
        media: [MediaRead] = [MediaRead(id=media_obj.id,
                                        type=media_obj.type,
                                        url=media_obj.url,
                                        thumbnail_url=media_obj.thumbnail_url,
                                        medium_thumbnail_url=media_obj.medium_thumbnail_url,
                                        order=media_obj.order)
                              for media_obj in db_media]

        return self.schema_read_with_media(**product.__dict__,
                                           media=media)

    def create(self, db: Session, product_create: schema_create) -> Optional[model]:
        # Generate thumbnail url, which is the first image's thumbnail url
        thumbnail_url = medium_thumbnail_url = ''
        for media_obj in product_create.media:
            if media_obj.type == MediaType.IMAGE:
                thumbnail_url, medium_thumbnail_url = media_obj.thumbnail_url, media_obj.medium_thumbnail_url

        # Create the product object
        product = self.model(id=get_random_alphanumeric_string(12),
                             thumbnail_url=thumbnail_url,
                             medium_thumbnail_url=medium_thumbnail_url,
                             **product_create.model_dump(exclude={"media", "thumbnail_url"}))

        db.add(product)
        db.commit()
        db.refresh(product)

        # Create the nested Media objects
        if product_create.media:
            i, media_objs = 0, []
            for media_obj in product_create.media:
                media_obj: MediaCreate = media_obj  # Add type support
                media_objs.append(Media(product_id=product.id,
                                        id=get_random_alphanumeric_string(20),
                                        type=media_obj.type,
                                        url=media_obj.url,
                                        thumbnail_url=media_obj.thumbnail_url,
                                        medium_thumbnail_url=media_obj.medium_thumbnail_url,
                                        order=i))

            db.bulk_save_objects(media_objs)
            db.commit()

        return self.get(db, product.id)

    def update(self, db: Session, db_obj: model, new_obj: schema_create) -> Optional[schema_read_with_media]:
        # Update the Product attributes
        update_dict: dict = new_obj.model_dump(exclude={"media", "thumbnail_url", "medium_thumbnail_url"})
        update_dict['thumbnail_url'] = new_obj.media[0].thumbnail_url if new_obj.media else ''
        update_dict['medium_thumbnail_url'] = new_obj.media[0].medium_thumbnail_url if new_obj.media else ''

        for key, value in update_dict.items():
            setattr(db_obj, key, value)

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

        return self.get(db, db_obj.id)

    def get_multi_with_filters(self, db: Session, offset: int, limit: int, show_status: [ProductStatus]) -> \
            (List)[schema_read_no_media]:
        products: List[AbstractCRUDProduct.model] = (db.query(self.model)
                                                     .filter(self.model.status.in_(show_status))
                                                     .order_by(desc(self.model.date_created))
                                                     .offset(offset)
                                                     .limit(limit)
                                                     .all())
        return [self.schema_read_no_media(**m.__dict__) for m in products]
