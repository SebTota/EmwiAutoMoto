import io
import uuid
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Query
from sqlalchemy.orm import Session
from PIL import Image as PIL_Image
from starlette import status

from backend import crud, models, schemas
from backend.enums import ProductStatusEnum
from backend.exceptions import FileUploadError
from backend.utils import deps
from backend.utils.image_handler import delete_image, process_image

router = APIRouter()


@router.get("", response_model=schemas.MotorcycleList)
def read_items(
        db: Session = Depends(deps.get_db),
        show_sold: bool = False,
        show_status: List[ProductStatusEnum] = Query(default=[ProductStatusEnum.active.value]),
        page: int = 1,
        limit: int = 8,
        current_user: Optional[models.User] = Depends(deps.get_current_active_superuser_if_signed_in),
) -> Any:
    """
    Retrieve motorcycle items.
    """
    if not (len(show_status) == 1 and show_status[0] == ProductStatusEnum.active.value) and not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this query",
        )

    return crud.motorcycle.get_multi_with_filters(db, page=page, limit=limit,
                                                  show_sold=show_sold, show_status=show_status)


@router.post("", response_model=schemas.Motorcycle)
def create_item(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.MotorcycleCreate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new motorcycle.
    """
    item = crud.motorcycle.create(db=db, obj_in=item_in)
    return item


@router.put("/{id}", response_model=schemas.Motorcycle)
def update_item(
        *,
        db: Session = Depends(deps.get_db),
        id: str,
        item_in: schemas.MotorcycleUpdate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a motorcycle.
    """
    item = crud.motorcycle.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="No motorcycle found with this id.")
    item = crud.motorcycle.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.post('/{id}/productImage')
def add_product_image(
        *,
        db: Session = Depends(deps.get_db),
        id: str,
        file: UploadFile,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Add a product image to a motorcycle.
    """
    motorcycle = crud.motorcycle.get(db=db, id=id)
    if not motorcycle:
        raise HTTPException(status_code=404, detail="No motorcycle found with this id.")

    image_content = file.file.read()
    img = PIL_Image.open(io.BytesIO(image_content))

    try:
        name: str = f'{str(uuid.uuid4())}.{file.filename.split(".")[-1]}'
        [image_url, thumbnail_url, medium_thumbnail_url] = process_image(img, name)
        img.close()
        file.file.close()

        # Set the photo as the thumbnail if the item doesn't already have a thumbnail
        if motorcycle.thumbnail_url is None:
            update: schemas.MotorcycleUpdate = schemas.MotorcycleUpdate(thumbnail_url=thumbnail_url,
                                                                        medium_thumbnail_url=medium_thumbnail_url)
            motorcycle = crud.motorcycle.update(db=db, db_obj=motorcycle, obj_in=update)

        image: schemas.ImageCreate = schemas.ImageCreate(image_url=image_url,
                                                         thumbnail_url=thumbnail_url,
                                                         medium_thumbnail_url=medium_thumbnail_url)
        i = crud.image.create_and_add_to_motorcycle(db=db, db_obj=motorcycle, obj_in=image)
        return i
    except FileUploadError as e:
        print(e)
        img.close()
        file.file.close()
        raise HTTPException(status_code=500, detail='Failed to process image.')


@router.get("/{id}", response_model=schemas.Motorcycle)
def read_item(
        *,
        db: Session = Depends(deps.get_db),
        id: str,
) -> Any:
    """
    Get item by ID.
    """
    item = crud.motorcycle.get(db=db, id=id)

    # TODO: Check if user is active if the motorcycle status is not active

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{id}", response_model=schemas.Motorcycle)
def delete_item(
        *,
        db: Session = Depends(deps.get_db),
        id: str,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an item.
    """
    item: schemas.Motorcycle = crud.motorcycle.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for image in item.images:
        delete_image(image)

    item = crud.motorcycle.remove(db=db, id=id)
    return item
