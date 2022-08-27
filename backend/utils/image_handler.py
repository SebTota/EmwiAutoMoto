import io
import os
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from PIL import Image

from backend.exceptions import FileUploadError

BUCKET_NAME = os.getenv('STORAGE_BUCKET_NAME')
BASE_HOST_URL = os.getenv('STORAGE_BASE_HOST_URL')


def _get_storage_resource() -> boto3.resource:
    return boto3.resource(service_name='s3',
                        endpoint_url= os.getenv('STORAGE_ENDPOINT_URL'),
                        aws_access_key_id=os.getenv('STORAGE_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('STORAGE_SECRET_ACCESS_KEY'),
                        config=Config(signature_version='s3v4'))


def upload_image_to_cloud_storage(image: Image, image_name: str) -> str:
    b2 = _get_storage_resource()

    buffer = io.BytesIO()
    image.save(buffer, format=image.format)
    buffer.seek(0)

    try:
        b2.Bucket(BUCKET_NAME).upload_fileobj(buffer, image_name)
        return f'{BASE_HOST_URL}/{image_name}'
    except Exception as e:
        raise FileUploadError(e)


def create_thumbnail_for_image(image: Image, image_name: str, size: [int, int] = None) -> str:
    if size is None:
        size = [350, 350]

    image_name = f'{size[0]}-{size[1]}-{image_name}'

    f = image.format
    img: Image = image.copy()
    img.thumbnail((size[0], size[1]))
    img.format = image.format

    return upload_image_to_cloud_storage(img, image_name)