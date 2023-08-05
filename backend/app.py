from dotenv import load_dotenv
load_dotenv()  # noqa

from fastapi import FastAPI

from backend.db.init_db import init_db
from backend.core.config import settings
from backend.api.v1.api import api_router

init_db()

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)
