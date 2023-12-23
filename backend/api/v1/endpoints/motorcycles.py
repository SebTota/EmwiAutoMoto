import io
import uuid
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from PIL import Image as PIL_Image

from backend import crud
from backend.models import User, MotorcycleStatus, Motorcycle
from backend.schemas import MotorcycleCreate, MotorcycleReadWithImages, MotorcycleReadNoImages, MotorcycleList
from backend.exceptions import FileUploadError
from backend.utils import deps
from backend.utils.image_handler import process_image

router = APIRouter()


@router.get("", response_model=MotorcycleList)
async def read_items(
        show_status: MotorcycleStatus = MotorcycleStatus.FOR_SALE,
        page: int = 1,
        limit: int = 12,
) -> Any:
    """
    Retrieve motorcycle items.
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than 0")

    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")

    offset: int = (page - 1) * limit
    items: List[MotorcycleReadNoImages] = await crud.motorcycle.get_multi_with_filters(offset, limit, [show_status])

    if not items:
        return MotorcycleList(page=page,
                              has_next_page=False,
                              motorcycles=[])

    has_next_page = True if len(items) == limit + 1 else False

    # Remove the extra motorcycle we got as a pagination test IFF there is a next page
    # (indicating we received +1 results back from db)
    if has_next_page:
        items.pop()

    return MotorcycleList(page=page,
                          has_next_page=has_next_page,
                          motorcycles=items)


@router.post("", response_model=MotorcycleReadWithImages)
async def create_item(
        item_in: MotorcycleCreate,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new motorcycle.
    """
    motorcycle = await crud.motorcycle.create(item_in)
    return motorcycle


@router.put("/{id}", response_model=MotorcycleReadWithImages)
async def update_item(
        id: str,
        item_in: MotorcycleCreate,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a motorcycle.
    """
    item: Optional[Motorcycle] = await crud.motorcycle.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="No motorcycle found with this id.")
    item = await crud.motorcycle.update(item, item_in)
    return item


# @router.post('/{id}/productImage', response_model=models.Image)
# def add_product_image(
#         *,
#         db: Session = Depends(deps.get_db),
#         id: str,
#         file: UploadFile,
#         current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Add a product image to a motorcycle.
#     """
#     motorcycle = crud.motorcycle.get(db, id)
#     if not motorcycle:
#         raise HTTPException(status_code=404, detail="No motorcycle found with this ID")
#
#     image_content = file.file.read()
#     img = PIL_Image.open(io.BytesIO(image_content))
#
#     try:
#         name: str = f'{str(uuid.uuid4())}.{file.filename.split(".")[-1]}'
#         motorcycle_image_sort_order: int = len(motorcycle.images) + 1
#         print(f"Image order: {motorcycle_image_sort_order}")
#
#         [image_url, thumbnail_url, medium_thumbnail_url] = process_image(img, name)
#         img.close()
#         file.file.close()
#
#         # Set the photo as the thumbnail if the item doesn't already have a thumbnail
#         if motorcycle.thumbnail_url is None or motorcycle.thumbnail_url == '':
#             update: models.MotorcycleUpdate = models.MotorcycleUpdate(thumbnail_url=thumbnail_url)
#             motorcycle = crud.motorcycle.update(db, motorcycle, update)
#
#         image: models.ImageCreate = models.ImageCreate(image_url=image_url,
#                                                        thumbnail_url=thumbnail_url,
#                                                        medium_thumbnail_url=medium_thumbnail_url,
#                                                        motorcycle_id=motorcycle.id,
#                                                        image_order=motorcycle_image_sort_order)
#         return crud.image.create(db, image)
#     except FileUploadError as e:
#         print(e)
#         img.close()
#         file.file.close()
#         raise HTTPException(status_code=500, detail='Failed to process image.')


@router.get("/{id}", response_model=MotorcycleReadWithImages)
async def read_item(id: str) -> Any:
    """
    Get item by ID.
    """
    # TODO: Check if user is active if the motorcycle status is not active
    item = await crud.motorcycle.get_with_images(id)
    if not item:
        raise HTTPException(status_code=404, detail="No motorcycle found with this ID")

    # m: MotorcycleReadWithImages = await MotorcycleReadWithImages.from_tortoise_orm(item)
    # print(m)
    # print(m.images)
    return item

# @router.delete("/{id}", response_model=models.MotorcycleRead)
# def delete_item(
#         *,
#         db: Session = Depends(deps.get_db),
#         id: str,
#         current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Delete an item.
#     """
#     item: models.Motorcycle = crud.motorcycle.get(db, id)
#     if not item:
#         raise HTTPException(status_code=404, detail="No motorcycle found with this ID")
#
#     # Mark item as deleted rather than deleting the item from the DB
#     update: models.MotorcycleUpdate = models.MotorcycleUpdate(status=models.MotorcycleStatus.deleted)
#
#     item = crud.motorcycle.update(db, item, update)
#     return item
