from tortoise.contrib.fastapi import register_tortoise

from backend.core.config import settings


def init_db(app) -> None:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={'models': ["backend.models"]},
    )
