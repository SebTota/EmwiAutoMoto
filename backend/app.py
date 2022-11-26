from dotenv import load_dotenv

load_dotenv()

from backend.db.session import SessionLocal
from backend.db.init_db import init_db

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic.main import BaseModel

from .routers import store, user, images

db = SessionLocal()
init_db(db)

app = FastAPI()
app.include_router(store.router, prefix='/store')
app.include_router(images.router, prefix='/store')
app.include_router(user.router)


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.get('/')
def root():
    return 'OK'
