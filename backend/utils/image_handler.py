import os
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

BUCKET_NAME = os.getenv('STORAGE_BUCKET_NAME')
BASE_HOST_URL = os.getenv('STORAGE_BASE_HOST_URL')


def _get_storage_resource() -> boto3.resource:
    return boto3.resource(service_name='s3',
                        endpoint_url= os.getenv('STORAGE_ENDPOINT_URL'),
                        aws_access_key_id=os.getenv('STORAGE_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('STORAGE_SECRET_ACCESS_KEY'),
                        config=Config(signature_version='s3v4'))


def upload_image_to_cloud_storage(image, image_name):
    b2 = _get_storage_resource()

    try:
        b2.Bucket(BUCKET_NAME).upload_fileobj(image, image_name)
        return f'{BASE_HOST_URL}/{image_name}'
    except ClientError as ce:
        print('error', ce)
    except Exception as e:
        print('error', e)


def create_thumbnail_for_image():
    return