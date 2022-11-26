import io
import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from PIL import Image as PIL_Image

from backend import crud, models, schemas
from backend.exceptions import FileUploadError
from backend.utils import deps
from backend.utils.image_handler import upload_image_to_cloud_storage, create_thumbnail_for_image

router = APIRouter()


@router.get("/", response_model=List[schemas.Motorcycle])
def read_items(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 15,
) -> Any:
    """
    Retrieve motorcycle items.
    """
    items = crud.motorcycle.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Motorcycle)
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
        # current_user: models.User = Depends(deps.get_current_active_superuser),
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
        thumbnail_url = create_thumbnail_for_image(img, name)
        image_url = upload_image_to_cloud_storage(img, name)
        img.close()
        file.file.close()

        image: schemas.ImageCreate = schemas.ImageCreate(image_url=image_url, thumbnail_url=thumbnail_url)
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
    item = crud.motorcycle.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.motorcycle.remove(db=db, id=id)
    return item
