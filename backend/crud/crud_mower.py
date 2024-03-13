from backend.crud.crud_product import AbstractCRUDProduct
from backend.models import Mower
from backend.schemas import MowerCreate, MowerReadWithMedia, MowerReadNoMedia


class MowerCRUD(AbstractCRUDProduct):
    model = Mower
    schema_create = MowerCreate
    schema_read_with_media = MowerReadWithMedia
    schema_read_no_media = MowerReadNoMedia


mower = MowerCRUD()
