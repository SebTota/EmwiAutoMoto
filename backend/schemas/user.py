from pydantic.main import BaseModel


class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    hashed_password: str
    is_superuser: bool


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
