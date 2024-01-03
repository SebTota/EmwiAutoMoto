import logging
import time

from fastapi import FastAPI, Request

# Configure logging
logging.basicConfig(
    level=logging.INFO
)

# Create a logger
logger = logging.getLogger(__name__)


def establish_request_detail_logging(app: FastAPI):
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