import os
from urllib.parse import quote

class Settings:
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = os.getenv('API_CREDENTIALS_GENERATOR_SECRET_KEY')
    REFRESH_TOKEN_SECRET_KEY: str = os.getenv('API_CREDENTIALS_REFRESH_TOKEN_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (60 * 24 * 14)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = (60 * 24 * 90)

    DATABASE_HOST: str = os.getenv('DATABASE_HOST')
    DATABASE_USER: str = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD: str = os.getenv('DATABASE_PASSWORD')
    DATABASE: str = os.getenv('DATABASE')
    DATABASE_URL: str = f'postgresql://{DATABASE_USER}:{quote(DATABASE_PASSWORD).encode()}@{DATABASE_HOST}/{DATABASE}'

    IMAGE_BUCKET_NAME: str = os.getenv('BUCKET_STORAGE_BUCKET_NAME')
    IMAGE_BUCKET_BASE_HOST_URL: str = os.getenv('BUCKET_STORAGE_OBJECT_BASE_URL')
    BUCKET_ENDPOINT_URL: str = os.getenv('BUCKET_STORAGE_ENDPOINT_URL')
    BUCKET_ACCESS_KEY_ID: str = os.getenv('BUCKET_STORAGE_ACCESS_KEY')
    BUCKET_SECRET_ACCESS_KEY: str = os.getenv('BUCKET_STORAGE_SECRET_ACCESS_KEY')


settings = Settings()
