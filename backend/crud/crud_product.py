from typing import Optional, List
from tortoise import transactions
from tortoise.queryset import QuerySet

from backend.models import Media
from backend.models.media import MediaType
from backend.models.product import Product, ProductStatus, ProductType
from backend.schemas import MediaRead, ProductReadWithMedia, ProductReadNoMedia, MediaCreate
from backend.schemas.product import ProductCreate
from backend.utils import get_random_alphanumeric_string


async def get(obj_id: str) -> Optional[Product]:
    return await Product.filter(id=obj_id).prefetch_related('media').first()


async def get_with_media(obj_id: str) -> Optional[ProductReadWithMedia]:
    async with transactions.in_transaction():
        product: Optional[Product] = await Product.filter(id=obj_id).first()

        if not product:
            return None

        # Preload and sort the Media
        db_media = await Media.filter(product=product).order_by("order").all()
        media: [MediaRead] = [MediaRead(id=media_obj.id,
                                        type=media_obj.type,
                                        url=media_obj.url,
                                        thumbnail_url=media_obj.thumbnail_url,
                                        medium_thumbnail_url=media_obj.medium_thumbnail_url,
                                        order=media_obj.order)
                              for media_obj in db_media]

        return ProductReadWithMedia(**product.__dict__,
                                    media=media)


async def create(product_create: ProductCreate) -> Optional[Product]:
    # Use transactions to ensure that the product and media are created together
    async with transactions.in_transaction():
        # Generate thumbnail url, which is the first image's thumbnail url
        thumbnail_url = medium_thumbnail_url = ''
        for media_obj in product_create.media:
            if media_obj.type == MediaType.IMAGE:
                thumbnail_url, medium_thumbnail_url = media_obj.thumbnail_url, media_obj.medium_thumbnail_url

        # Create the product object
        product = await Product.create(id=get_random_alphanumeric_string(12),
                                       thumbnail_url=thumbnail_url,
                                       medium_thumbnail_url=medium_thumbnail_url,
                                       **product_create.dict(exclude={"media", "thumbnail_url"}))

        # Create the nested Media objects
        if product_create.media:
            i, media_objs = 0, []
            for media_obj in product_create.media:
                media_obj: MediaCreate = media_obj  # Add type support
                media_objs.append(Media(product=product,
                                        id=get_random_alphanumeric_string(20),
                                        type=media_obj.type,
                                        url=media_obj.url,
                                        thumbnail_url=media_obj.thumbnail_url,
                                        medium_thumbnail_url=media_obj.medium_thumbnail_url,
                                        order=i))

            await Media.bulk_create(media_objs)

    return await get(product.id)


async def update(db_obj: Product, new_obj: ProductCreate) -> Optional[ProductReadWithMedia]:
    # Update the Product attributes
    update_dict: dict = new_obj.model_dump(exclude={"media", "thumbnail_url", "medium_thumbnail_url"})
    update_dict['thumbnail_url'] = new_obj.media[0].thumbnail_url if new_obj.media else ''
    update_dict['medium_thumbnail_url'] = new_obj.media[0].medium_thumbnail_url if new_obj.media else ''

    await db_obj.update_from_dict(update_dict)
    await db_obj.save()

    async with transactions.in_transaction():
        for media_obj in db_obj.media:
            # TODO: Make sure we remove any actually deleted items from object storage
            await media_obj.delete()

        if new_obj.media:
            i, media_objs = 0, []
            for media_obj in new_obj.media:
                media_obj: MediaCreate = media_obj  # Add type support
                media_objs.append(Media(product=db_obj,
                                        id=get_random_alphanumeric_string(20),
                                        type=media_obj.type,
                                        url=media_obj.url,
                                        thumbnail_url=media_obj.thumbnail_url,
                                        medium_thumbnail_url=media_obj.medium_thumbnail_url,
                                        order=i))
                i += 1

            await Media.bulk_create(media_objs)

    return await get(db_obj.id)


async def get_multi_with_filters(product_type: ProductType, offset: int, limit: int, show_status: [ProductStatus]) -> \
        List[ProductReadNoMedia]:
    query: QuerySet = (Product.filter(type=product_type)
                       .filter(status__in=show_status)
                       .offset(offset)
                       .limit(limit)
                       .order_by("-date_created"))
    products: List[Product] = await query
    return [ProductReadNoMedia(**m.__dict__) for m in products]
