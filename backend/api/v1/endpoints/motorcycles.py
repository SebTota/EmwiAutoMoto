import concurrent.futures
import io
import uuid
from typing import Any, List, Optional

from backend.core.logging import logger
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Query, BackgroundTasks
from PIL import Image as PIL_Image

from backend import crud
from backend.models import User, MotorcycleStatus, Motorcycle
from backend.schemas import MotorcycleCreate, MotorcycleReadWithImages, MotorcycleReadNoImages, MotorcycleList, \
    ImageRead
from backend.exceptions import FileUploadError
from backend.utils import deps
from backend.utils.image_handler import process_image

router = APIRouter()


@router.get("", response_model=MotorcycleList)
async def read_items(
        show_status: List[MotorcycleStatus] = Query([MotorcycleStatus.FOR_SALE]),
        page: int = 1,
        limit: int = 12,
        current_user: User = Depends(deps.get_current_active_superuser_no_exception),
) -> Any:
    """
    Retrieve motorcycle items.
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than 0")

    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")

    if len(show_status) == 1 and show_status[0] == MotorcycleStatus.FOR_SALE:
        ...
    else:
        if not current_user or not current_user.is_superuser:
            raise HTTPException(status_code=403, detail="You must be a superuser to view these items")

    offset: int = (page - 1) * limit

    # Add 1 to the limit to see if there is a next page.
    items: List[MotorcycleReadNoImages] = await crud.motorcycle.get_multi_with_filters(offset, limit + 1, show_status)

    if not items:
        return MotorcycleList(page=page,
                              has_next_page=False,
                              motorcycles=[])

    has_next_page = True if len(items) > limit else False

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


@router.post('/image', response_model=List[ImageRead])
def generate_product_images(
        files: List[UploadFile],
        background_tasks: BackgroundTasks,
        current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    def process_single_image(file):
        image_content = file.file.read()
        img = PIL_Image.open(io.BytesIO(image_content))

        try:
            name: str = f'{str(uuid.uuid4())}.{file.filename.split(".")[-1]}'
            [image_url, thumbnail_url, medium_thumbnail_url] = process_image(img, name)
            img.close()
            file.file.close()
            return ImageRead(image_url=image_url,
                             thumbnail_url=thumbnail_url,
                             medium_thumbnail_url=medium_thumbnail_url)
        except FileUploadError as e:
            logger.error("Failed to process image.", e)
            img.close()
            file.file.close()
            raise HTTPException(status_code=500, detail='Failed to process image.')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        image_results = list(executor.map(process_single_image, files))

    return image_results


@router.get("/{id}", response_model=MotorcycleReadWithImages)
async def read_item(id: str) -> Any:
    """
    Get item by ID.
    """
    # TODO: Check if user is active if the motorcycle status is not active
    item = await crud.motorcycle.get_with_images(id)
    if not item:
        raise HTTPException(status_code=404, detail="No motorcycle found with this ID")
    return item

