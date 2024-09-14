from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend import crud
from backend.api.v1.endpoints.products.products import AbstractProductAPI
from backend.db.init_db import get_db
from backend.models import Motorcycle, User
from backend.schemas import MotorcycleCreate, MotorcycleReadNoMedia, MotorcycleReadWithMedia, MotorcycleList, \
    VehicleAIRecommendation
from backend.services import get_ai_description_for_vehicle
from backend.utils import deps


class MotorcycleAPI(AbstractProductAPI):
    @classmethod
    def setup_routes(cls):
        router = super().setup_routes(
            crud_class=crud.motorcycle,
            product_model=Motorcycle,
            schema_product_create=MotorcycleCreate,
            schema_product_read_no_media=MotorcycleReadNoMedia,
            schema_product_read_with_media=MotorcycleReadWithMedia,
            schema_product_list=MotorcycleList
        )

        @router.get("/{id}/ai-recommendation", response_model=VehicleAIRecommendation)
        def get_ai_recommendation(
                id: str,
                db: Session = Depends(get_db),
                current_user: User = Depends(deps.get_current_active_superuser),
        ):
            """
            Get AI recommendation for Motorcycle entry
            """
            item = crud.motorcycle.get_with_media(db, id)

            if not item:
                raise HTTPException(status_code=404, detail="No product found with this ID")

            return get_ai_description_for_vehicle(item)

        return router


motorcycle_router = MotorcycleAPI.setup_routes()
