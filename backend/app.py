from backend.core.logging import establish_request_detail_logging
from backend.core.logging import logger  # noqa

from dotenv import load_dotenv
import os
env_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.env'))  # noqa
load_dotenv(dotenv_path=env_path)  # noqa

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from backend.db.init_db import init_db
from backend.core.config import settings
from backend.api.v1.api import api_router

app: FastAPI = FastAPI()
init_db(app)
establish_request_detail_logging(app)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://localhost:5173", "https://emwiautomoto.sebtota.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
