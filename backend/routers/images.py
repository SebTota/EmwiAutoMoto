from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_jwt_auth import AuthJWT

from backend.utils.image_handler import upload_image_to_cloud_storage

router = APIRouter(tags=["Images"])


@router.post('/productImage')
def upload_product_image(image: UploadFile, Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    return upload_image_to_cloud_storage(image.file, image.filename)
