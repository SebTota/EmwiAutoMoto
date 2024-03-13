import concurrent.futures
import io
import uuid
from typing import Any, List, Optional
from sqlalchemy.orm import Session

from backend.core.logging import logger
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Query, BackgroundTasks
from PIL import Image as PIL_Image

from backend import crud
from backend.db.init_db import get_db
from backend.models import User, ProductStatus, Motorcycle, MediaType
from backend.schemas import MediaRead, MotorcycleReadWithMedia, MotorcycleReadNoMedia, MotorcycleList, MotorcycleCreate
from backend.exceptions import FileUploadError
from backend.utils import deps
from backend.utils.image_handler import process_image

router = APIRouter()


@router.get("", response_model=MotorcycleList)
def read_items(
        show_status: List[ProductStatus] = Query([ProductStatus.FOR_SALE]),
        page: int = 1,
        limit: int = 12,
        db: Session = Depends(get_db),
        current_user: User = Depends(deps.get_current_active_superuser_no_exception),
) -> Any:
    """
    Retrieve motorcycles with specified filters.
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than 0")

    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")

    if ProductStatus.DELETED in show_status or ProductStatus.DRAFT in show_status:
        if not current_user or not current_user.is_superuser:
            raise HTTPException(status_code=403, detail="You must be a superuser to view these items")

    offset: int = (page - 1) * limit

    # Add 1 to the limit to see if there is a next page.
    items: List[MotorcycleReadNoMedia] = crud.motorcycle.get_multi_with_filters(db, offset,
                                                                                limit + 1,
                                                                                show_status)

    if not items:
        return MotorcycleList(page=page,
                              has_next_page=False,
                              motorcycles=[])

    has_next_page = True if len(items) > limit else False

    # Remove the extra motorcycles we got as a pagination test IFF there is a next page
    # (indicating we received +1 results back from db)
    if has_next_page:
        items.pop()

    return MotorcycleList(page=page,
                          has_next_page=has_next_page,
                          motorcycles=items)


@router.post("", response_model=MotorcycleReadWithMedia)
def create_item(
        item_in: MotorcycleCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new motorcycle.
    """
    return crud.motorcycle.create(db, item_in)


@router.put("/{id}", response_model=MotorcycleReadWithMedia)
def update_item(
        id: str,
        item_in: MotorcycleCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a motorcycle.
    """
    item: Optional[Motorcycle] = crud.motorcycle.get(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="No motorcycle found with this id.")
    item = crud.motorcycle.update(db, item, item_in)
    return item


@router.post('/image', response_model=List[MediaRead])
def generate_motorcycle_images(
        files: List[UploadFile],
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
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
            return MediaRead(type=MediaType.IMAGE,
                             url=image_url,
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


@router.get("/{id}", response_model=MotorcycleReadWithMedia)
def read_item(
        id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(deps.get_current_active_superuser_no_exception), ) -> Any:
    """
    Get item by ID.
    """
    # TODO: Check if user is active if the product status is not active
    item = crud.motorcycle.get_with_media(db, id)

    if item.status in [ProductStatus.DRAFT, ProductStatus.DELETED]:
        if not current_user or not current_user.is_superuser:
            raise HTTPException(status_code=403, detail="You must be a superuser to view this item")

    if not item:
        raise HTTPException(status_code=404, detail="No motorcycle found with this ID")
    return item
