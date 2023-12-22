from pydantic.main import BaseModel


class UserRead(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_superuser: bool


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
