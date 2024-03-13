from backend import crud
from backend.api.v1.endpoints.products.products import AbstractProductAPI
from backend.models import Mower
from backend.schemas import MowerCreate, MowerReadNoMedia, MowerReadWithMedia, MowerList


class MowerAPI(AbstractProductAPI):
    @classmethod
    def setup_routes(cls):
        return super().setup_routes(
            crud_class=crud.mower,
            product_model=Mower,
            schema_product_create=MowerCreate,
            schema_product_read_no_media=MowerReadNoMedia,
            schema_product_read_with_media=MowerReadWithMedia,
            schema_product_list=MowerList
        )


mower_router = MowerAPI.setup_routes()
