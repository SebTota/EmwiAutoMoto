import logging
import time

from dotenv import load_dotenv
import os
env_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.env'))  # noqa
load_dotenv(dotenv_path=env_path)  # noqa

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from backend.db.init_db import init_db
from backend.core.config import settings
from backend.api.v1.api import api_router

app = FastAPI()
init_db(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Create a logger
logger = logging.getLogger(__name__)

# Middleware for logging request and response times
@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"Path: {request.url.path}, Method: {request.method}, "
        f"Status Code: {response.status_code}, "
        f"Process Time: {process_time:.5f} seconds"
    )

    return response

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://localhost:5173", "https://emwiautomoto.sebtota.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
