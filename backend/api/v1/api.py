from fastapi import APIRouter

from backend.api.v1.endpoints import login, users, products

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.image_router, prefix="/products/images", tags=["images"])
api_router.include_router(products.motorcycle_router, prefix="/products/motorcycles", tags=["products", "motorcycles"])
api_router.include_router(products.mower_router, prefix="/products/mowers", tags=["products", "mowers"])
api_router.include_router(products.part_router, prefix="/products/parts", tags=["products", "parts"])
