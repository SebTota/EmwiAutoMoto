from fastapi import APIRouter

from backend.api.v1.endpoints import login, users, motorcycles, contact

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(motorcycles.router, prefix="/motorcycles", tags=["motorcycles"])
api_router.include_router(contact.router, prefix='/contact', tags=['contact'])
