from backend.core.logging import establish_request_detail_logging
from backend.core.logging import logger  # noqa

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.db.init_db import init_db
from backend.core.config import settings
from backend.api.v1.api import api_router

app: FastAPI = FastAPI()
init_db(app)
establish_request_detail_logging(app)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost",
                       "http://localhost:5173",
                       "https://emwiautomoto.sebtota.com",
                       "https://emwiautomoto.pl"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
