from backend import crud
from backend.api.v1.endpoints.products.products import AbstractProductAPI
from backend.models import Motorcycle
from backend.schemas import MotorcycleCreate, MotorcycleReadNoMedia, MotorcycleReadWithMedia, MotorcycleList


class MotorcycleAPI(AbstractProductAPI):
    @classmethod
    def setup_routes(cls):
        return super().setup_routes(
            crud_class=crud.motorcycle,
            product_model=Motorcycle,
            schema_product_create=MotorcycleCreate,
            schema_product_read_no_media=MotorcycleReadNoMedia,
            schema_product_read_with_media=MotorcycleReadWithMedia,
            schema_product_list=MotorcycleList
        )


motorcycle_router = MotorcycleAPI.setup_routes()
