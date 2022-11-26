import os
import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (60 * 24 * 8)
    DATABASE_PASSWORD: str = os.getenv('DATABASE_PASSWORD')
    DATABASE_URL: str = f'postgresql://postgres:{DATABASE_PASSWORD}@198.46.142.2/emwi_auto_moto'


settings = Settings()
