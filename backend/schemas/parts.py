from typing import List

from backend.schemas.product import ProductBase, ProductCreate, ProductList


class PartBase(ProductBase):
    pass


class PartReadWithMedia(ProductBase):
    pass


class PartReadNoMedia(ProductBase):
    pass


class PartCreate(ProductCreate):
    pass


class PartList(ProductList):
    page: int
    has_next_page: bool
    products: List[PartReadNoMedia]
