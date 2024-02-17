from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

from backend.core.config import settings

# For aerich migrations
TORTOISE_ORM = {
    "connections": {
        "default": settings.DATABASE_URL,
    },
    "apps": {
        "models": {"models": ["backend.models", "aerich.models"], "default_connection": "default"},
    },
}


def init_db(app) -> None:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={'models': ["backend.models", "aerich.models"]},
    )


async def init_db_for_script():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={'models': ['backend.models']},
    )
