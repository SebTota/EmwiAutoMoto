from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend import crud
from backend.api.v1.endpoints.products.products import AbstractProductAPI
from backend.db.init_db import get_db
from backend.models import Motorcycle, User
from backend.schemas import MotorcycleCreate, MotorcycleReadNoMedia, MotorcycleReadWithMedia, MotorcycleList, \
    VehicleDetailRecommendation
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

        @router.get("/{id}/product-detail-recommendation", response_model=MotorcycleReadWithMedia)
        def get_ai_recommendation(
                id: str,
                db: Session = Depends(get_db),
                current_user: User = Depends(deps.get_current_active_superuser),
        ):
            """
            Get AI recommendation for Motorcycle entry
            """
            db_item: Optional[Motorcycle] = crud.motorcycle.get_with_media(db, id)

            if not db_item:
                raise HTTPException(status_code=404, detail="No product found with this ID")

            # Create Schema copy of DB item, so we are not updating the DB item with temp changes
            item: MotorcycleReadWithMedia = MotorcycleReadWithMedia(**db_item.__dict__)

            # Generate recommendations
            suggestion: VehicleDetailRecommendation = get_ai_description_for_vehicle(item)
            item.make = suggestion.make
            item.model = suggestion.model
            item.color = suggestion.color
            item.description = suggestion.description

            item.title = f"{item.year} {suggestion.make}"
            item.subtitle = suggestion.model

            return item

        return router


motorcycle_router = MotorcycleAPI.setup_routes()
