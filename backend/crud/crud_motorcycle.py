from typing import Optional
from tortoise import transactions

from backend.models import Image
from backend.models.motorcycle import Motorcycle
from backend.schemas import ImageRead, MotorcycleReadWithImages, ImageCreate
from backend.schemas.motorcycle import MotorcycleCreate
from backend.utils import get_random_alphanumeric_string


async def get(obj_id: str) -> Optional[MotorcycleReadWithImages]:
    async with transactions.in_transaction():
        motorcycle: Optional[Motorcycle] = await Motorcycle.filter(id=obj_id).first()

        if not motorcycle:
            return None

        # Preload and sort the images
        db_images = await Image.filter(motorcycle=motorcycle).order_by("order").all()
        images: [ImageRead] = [ImageRead(id=img.id,
                                         image_url=img.image_url,
                                         thumbnail_url=img.thumbnail_url,
                                         medium_thumbnail_url=img.medium_thumbnail_url,
                                         order=img.order)
                               for img in db_images]

        return MotorcycleReadWithImages(id=motorcycle.id,
                                        date_created=motorcycle.date_created,
                                        date_last_updated=motorcycle.date_last_updated,
                                        year=motorcycle.year,
                                        make=motorcycle.make,
                                        model=motorcycle.model,
                                        odometer_miles=motorcycle.odometer_miles,
                                        color=motorcycle.color,
                                        price=motorcycle.price,
                                        description=motorcycle.description,
                                        status=motorcycle.status,
                                        thumbnail_url=motorcycle.thumbnail_url,
                                        medium_thumbnail_url=motorcycle.medium_thumbnail_url,
                                        images=images)


async def create(motorcycle_create: MotorcycleCreate) -> Optional[Motorcycle]:
    # Use transactions to ensure that the motorcycle and images are created together
    async with transactions.in_transaction():
        # Generate thumbnail url, which is the first image's thumbnail url
        thumbnail_url = motorcycle_create.images[0].thumbnail_url if motorcycle_create.images else ''
        medium_thumbnail_url = motorcycle_create.images[0].medium_thumbnail_url if motorcycle_create.images else ''

        # Create the motorcycle object
        motorcycle = await Motorcycle.create(id=get_random_alphanumeric_string(12),
                                             thumbnail_url=thumbnail_url,
                                             medium_thumbnail_url=medium_thumbnail_url,
                                             **motorcycle_create.dict(exclude={"images", "thumbnail_url"}))

        # Create the nested Image objects
        if motorcycle_create.images:
            i, images = 0, []
            for image in motorcycle_create.images:
                image: ImageCreate = image
                images.append(Image(motorcycle=motorcycle,
                                    id=get_random_alphanumeric_string(20),
                                    image_url=image.image_url,
                                    thumbnail_url=image.thumbnail_url,
                                    medium_thumbnail_url=image.medium_thumbnail_url,
                                    order=i))

            await Image.bulk_create(images)

        return await get(motorcycle.id)

# def update(db: Session, db_obj: Motorcycle, obj_update: MotorcycleUpdate) -> Motorcycle:
#     obj_update_data = obj_update.dict(exclude_unset=True)
#
#     # Update the simple attributes of Motorcycle
#     for k, v in obj_update_data.items():
#         if k != "images":
#             setattr(db_obj, k, v)
#
#     # Handle the images relationship separately
#     if "images" in obj_update_data:
#         updated_image_ids: [str] = [image.id for image in obj_update.images]
#         removed_image_ids: [str] = []
#         for image in db_obj.images:
#             if image.id not in updated_image_ids:
#                 removed_image_ids.append(image.id)
#
#         print(f'Removing images: {removed_image_ids} for motorcycle id: {db_obj.id}')
#
#         for removed_image_id in removed_image_ids:
#             # TODO: Also remove the image from object storage
#             db.query(Image).filter(Image.id == removed_image_id).delete()
#
#     # TODO: Update the thumbnail url if the thumbnail image was removed
#
#     db.commit()
#     db.refresh(db_obj)
#     return db_obj


# def get_multi_with_filters(db: Session, offset: int = 0, limit: int = 100,
#                            show_status: MotorcycleStatus = MotorcycleStatus.for_sale.value) -> List[Motorcycle]:
#     return db.query(Motorcycle) \
#         .filter(Motorcycle.status == show_status)\
#         .order_by(Motorcycle.date_created)\
#         .offset(offset)\
#         .limit(limit)\
#         .all()
