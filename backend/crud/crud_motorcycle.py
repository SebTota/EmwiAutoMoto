from typing import Optional, List
from tortoise import transactions
from tortoise.queryset import QuerySet

from backend.models import Image
from backend.models.motorcycle import Motorcycle, MotorcycleStatus
from backend.schemas import ImageRead, MotorcycleReadWithImages, MotorcycleReadNoImages, ImageCreate
from backend.schemas.motorcycle import MotorcycleCreate
from backend.utils import get_random_alphanumeric_string


async def get(obj_id: str) -> Optional[Motorcycle]:
    return await Motorcycle.filter(id=obj_id).prefetch_related('images').first()

async def get_with_images(obj_id: str) -> Optional[MotorcycleReadWithImages]:
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


async def update(db_obj: Motorcycle, new_obj: MotorcycleCreate) -> Optional[MotorcycleReadWithImages]:
    # Update the Motorcycle attributes
    update_dict: dict = new_obj.model_dump(exclude={"images", "thumbnail_url", "medium_thumbnail_url"})
    update_dict['thumbnail_url'] = new_obj.images[0].thumbnail_url if new_obj.images else ''
    update_dict['medium_thumbnail_url'] = new_obj.images[0].medium_thumbnail_url if new_obj.images else ''

    await db_obj.update_from_dict(update_dict)
    await db_obj.save()

    async with transactions.in_transaction():
        for image in db_obj.images:
            # TODO: Make sure we remove any actually deleted items from object storage
            await image.delete()

        if new_obj.images:
            i, images = 0, []
            for image in new_obj.images:
                image: ImageCreate = image
                images.append(Image(motorcycle=db_obj,
                                    id=get_random_alphanumeric_string(20),
                                    image_url=image.image_url,
                                    thumbnail_url=image.thumbnail_url,
                                    medium_thumbnail_url=image.medium_thumbnail_url,
                                    order=i))

            await Image.bulk_create(images)

    return await get(db_obj.id)


async def get_multi_with_filters(offset: int, limit: int, show_status: [MotorcycleStatus]) -> List[MotorcycleReadNoImages]:
    query: QuerySet = (Motorcycle.filter(status__in=show_status)
                       .offset(offset)
                       .limit(limit)
                       .order_by("-date_created"))
    motorcycles: List[Motorcycle] = await query
    return [MotorcycleReadNoImages(**m.__dict__) for m in motorcycles]
