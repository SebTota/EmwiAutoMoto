from typing import Optional, List
from tortoise import transactions
from tortoise.queryset import QuerySet

from backend.models import Image
from backend.models.product import Product, ProductStatus
from backend.schemas import ImageRead, ProductReadWithImages, ProductReadNoImages, ImageCreate
from backend.schemas.product import ProductCreate
from backend.utils import get_random_alphanumeric_string


async def get(obj_id: str) -> Optional[Product]:
    return await Product.filter(id=obj_id).prefetch_related('images').first()


async def get_with_images(obj_id: str) -> Optional[ProductReadWithImages]:
    async with transactions.in_transaction():
        product: Optional[Product] = await Product.filter(id=obj_id).first()

        if not product:
            return None

        # Preload and sort the images
        db_images = await Image.filter(product=product).order_by("order").all()
        images: [ImageRead] = [ImageRead(id=img.id,
                                         image_url=img.image_url,
                                         thumbnail_url=img.thumbnail_url,
                                         medium_thumbnail_url=img.medium_thumbnail_url,
                                         order=img.order)
                               for img in db_images]

        return ProductReadWithImages(**product.__dict__,
                                     images=images)


async def create(product_create: ProductCreate) -> Optional[Product]:
    # Use transactions to ensure that the product and images are created together
    async with transactions.in_transaction():
        # Generate thumbnail url, which is the first image's thumbnail url
        thumbnail_url = product_create.images[0].thumbnail_url if product_create.images else ''
        medium_thumbnail_url = product_create.images[0].medium_thumbnail_url if product_create.images else ''

        # Create the product object
        product = await Product.create(id=get_random_alphanumeric_string(12),
                                       thumbnail_url=thumbnail_url,
                                       medium_thumbnail_url=medium_thumbnail_url,
                                       **product_create.dict(exclude={"images", "thumbnail_url"}))

        # Create the nested Image objects
        if product_create.images:
            i, images = 0, []
            for image in product_create.images:
                image: ImageCreate = image
                images.append(Image(product=product,
                                    id=get_random_alphanumeric_string(20),
                                    image_url=image.image_url,
                                    thumbnail_url=image.thumbnail_url,
                                    medium_thumbnail_url=image.medium_thumbnail_url,
                                    order=i))

            await Image.bulk_create(images)

    return await get(product.id)


async def update(db_obj: Product, new_obj: ProductCreate) -> Optional[ProductReadWithImages]:
    # Update the Product attributes
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
                images.append(Image(product=db_obj,
                                    id=get_random_alphanumeric_string(20),
                                    image_url=image.image_url,
                                    thumbnail_url=image.thumbnail_url,
                                    medium_thumbnail_url=image.medium_thumbnail_url,
                                    order=i))
                i += 1

            await Image.bulk_create(images)

    return await get(db_obj.id)


async def get_multi_with_filters(offset: int, limit: int, show_status: [ProductStatus]) -> List[ProductReadNoImages]:
    query: QuerySet = (Product.filter(status__in=show_status)
                       .offset(offset)
                       .limit(limit)
                       .order_by("-date_created"))
    products: List[Product] = await query
    return [ProductReadNoImages(**m.__dict__) for m in products]
