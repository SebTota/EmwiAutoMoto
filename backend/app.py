from dotenv import load_dotenv
import os
env_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '.env'))  # noqa
load_dotenv(dotenv_path=env_path)  # noqa

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.db.session import SessionLocal
from backend.db.init_db import init_db
from backend.core.config import settings
from backend.api.v1.api import api_router

db = SessionLocal()
init_db(db)

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
