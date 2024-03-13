from backend.crud.crud_product import AbstractCRUDProduct
from backend.models import Part
from backend.schemas import PartCreate, PartReadWithMedia, PartReadNoMedia


class PartCRUD(AbstractCRUDProduct):
    model = Part
    schema_create = PartCreate
    schema_read_with_media = PartReadWithMedia
    schema_read_no_media = PartReadNoMedia


part = PartCRUD()
