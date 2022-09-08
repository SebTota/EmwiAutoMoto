import io
import uuid
from PIL import Image as PIL_Image
from fastapi import APIRouter, Depends, UploadFile
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT

from backend.utils.image_handler import upload_image_to_cloud_storage, create_thumbnail_for_image, delete_image
from backend.models.schemas import UploadImageResponse, Image
from backend.exceptions.FileUploadError import FileUploadError

router = APIRouter(tags=["Images"])


@router.post('/productImage', response_model=UploadImageResponse, status_code=201)
def upload_product_image_route(file: UploadFile, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    image_content = file.file.read()
    img = PIL_Image.open(io.BytesIO(image_content))

    try:
        name: str = str(uuid.uuid4())
        thumbnail_url = create_thumbnail_for_image(img, name)
        image_url = upload_image_to_cloud_storage(img, name)
        img.close()
        file.file.close()
        return UploadImageResponse(thumbnail=thumbnail_url, image=image_url)
    except FileUploadError as e:
        img.close()
        file.file.close()
        raise HTTPException(status_code=500, detail='Failed to process image.')
    finally:
        img.close()
        file.file.close()


@router.delete('/productImage')
def delete_image_route(image: Image, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    delete_image(image)
