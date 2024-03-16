from typing import List

from backend.schemas.product import ProductBase, ProductCreate, ProductList, ProductReadNoMedia, ProductReadWithMedia


class PartBase(ProductBase):
    pass


class PartReadWithMedia(ProductReadWithMedia):
    pass


class PartReadNoMedia(ProductReadNoMedia):
    pass


class PartCreate(ProductCreate):
    pass


class PartList(ProductList):
    page: int
    has_next_page: bool
    products: List[PartReadNoMedia]
