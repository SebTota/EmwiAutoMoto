import io
import mimetypes
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed

import boto3
from botocore.config import Config
from PIL import Image as PIL_Image

from backend.core.config import settings
from backend.exceptions import FileUploadError
from backend.models import Image

BUCKET_NAME = settings.IMAGE_BUCKET_NAME
BASE_HOST_URL = settings.IMAGE_BUCKET_BASE_HOST_URL

THUMBNAIL_SIZE = [400, 400]
MEDIUM_THUMBNAIL_SIZE = [900, 900]


def _get_storage_resource() -> boto3.resource:
    return boto3.resource(service_name='s3',
                          endpoint_url=settings.BUCKET_ENDPOINT_URL,
                          aws_access_key_id=settings.BUCKET_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.BUCKET_SECRET_ACCESS_KEY,
                          config=Config(signature_version='s3v4'))


def _get_s3_client() -> boto3.client:
    return boto3.client(service_name='s3',
                        endpoint_url=settings.BUCKET_ENDPOINT_URL,
                        aws_access_key_id=settings.BUCKET_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.BUCKET_SECRET_ACCESS_KEY,
                        config=Config(signature_version='s3v4'))


def process_image(image: PIL_Image, image_name: str):
    sizes = [None, THUMBNAIL_SIZE, MEDIUM_THUMBNAIL_SIZE]

    with ProcessPoolExecutor(3) as exe:
        futures = [exe.submit(_thread_process_image_task, image, image_name, size) for size in sizes]

    urls = [None, None, None]  # original, thumbnail, medium thumbnail

    for future in as_completed(futures):
        url: str = future.result()

        if f'{THUMBNAIL_SIZE[0]}-{THUMBNAIL_SIZE[1]}-{image_name}' in url:
            urls[1] = url
        elif f'{MEDIUM_THUMBNAIL_SIZE[0]}-{MEDIUM_THUMBNAIL_SIZE[1]}-{image_name}' in url:
            urls[2] = url
        else:
            urls[0] = url

    return urls


def _thread_process_image_task(image: PIL_Image, name: str, size: [int, int] = None) -> str:
    if not size:
        url = upload_image_to_cloud_storage(image, name)
    else:
        url = create_thumbnail_for_image(image, name, size)

    return url


def upload_image_to_cloud_storage(image: PIL_Image, image_name: str) -> str:
    s3 = _get_storage_resource()

    buffer = io.BytesIO()
    image.save(buffer, format=image.format)
    buffer.seek(0)

    # Use mimetypes to determine the content type dynamically
    content_type, _ = mimetypes.guess_type(image_name)

    try:
        print(f"Uploading file: {image_name} to cloud storage...")
        s3.Bucket(BUCKET_NAME).upload_fileobj(buffer, image_name, ExtraArgs={'ContentType': content_type,
                                                                             'CacheControl': 'max-age=31536000'})
        print(f"Upload of file: {image_name} complete!")
        return f'{BASE_HOST_URL}/{image_name}'
    except Exception as e:
        raise FileUploadError(e)


def create_thumbnail_for_image(image: PIL_Image, image_name: str, size: [int, int]) -> str:
    image_name = f'{size[0]}-{size[1]}-{image_name}'

    img: PIL_Image = image.copy()
    img.thumbnail((size[0], size[1]))
    img.format = image.format

    r = upload_image_to_cloud_storage(img, image_name)
    img.close()
    return r


def delete_image(image: Image):
    s3: boto3.client = _get_s3_client()
    s3.delete_objects(Bucket=BUCKET_NAME, Delete={
        'Objects': [
            {'Key': image.image_url.split('/')[-1]},
            {'Key': image.thumbnail_url.split('/')[-1]}
        ]
    })
