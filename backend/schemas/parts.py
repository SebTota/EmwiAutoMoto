from backend.schemas.product import ProductBase, ProductCreate


class PartsBase(ProductBase):
    pass


class PartsReadWithMedia(ProductBase):
    pass


class PartsReadNoMedia(ProductBase):
    pass


class PartsCreate(ProductCreate):
    pass

