from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

from backend.core.config import settings


def init_db(app) -> None:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={'models': ["backend.models"]},
    )

async def init_db_for_script():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={'models': ['backend.models']},
    )
