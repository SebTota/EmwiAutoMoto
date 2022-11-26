from dotenv import load_dotenv
load_dotenv()  # noqa

from fastapi import FastAPI

from backend.db.session import SessionLocal
from backend.db.init_db import init_db
from backend.core.config import settings
from backend.api.v1.api import api_router

db = SessionLocal()
init_db(db)

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)
