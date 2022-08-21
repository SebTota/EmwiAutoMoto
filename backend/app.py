from fastapi import FastAPI, APIRouter
from starlette.middleware.sessions import SessionMiddleware
import os

from .routers import store

app = FastAPI()
app.include_router(store.router, prefix='/store')


@app.get('/')
def root():
    return 'OK'
