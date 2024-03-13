from backend.crud.crud_product import AbstractCRUDProduct
from backend.models import Motorcycle
from backend.schemas import MotorcycleCreate, MotorcycleReadWithMedia, MotorcycleReadNoMedia


class MotorcycleCRUD(AbstractCRUDProduct):
    model = Motorcycle
    schema_create = MotorcycleCreate
    schema_read_with_media = MotorcycleReadWithMedia
    schema_read_no_media = MotorcycleReadNoMedia


motorcycle = MotorcycleCRUD()
