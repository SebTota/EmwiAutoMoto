from backend import crud
from backend.api.v1.endpoints.products.products import AbstractProductAPI
from backend.models import Part
from backend.schemas import PartCreate, PartReadNoMedia, PartReadWithMedia, PartList


class PartAPI(AbstractProductAPI):
    @classmethod
    def setup_routes(cls):
        return super().setup_routes(
            crud_class=crud.part,
            product_model=Part,
            schema_product_create=PartCreate,
            schema_product_read_no_media=PartReadNoMedia,
            schema_product_read_with_media=PartReadWithMedia,
            schema_product_list=PartList
        )


part_router = PartAPI.setup_routes()
