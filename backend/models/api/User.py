from pydantic.main import BaseModel


class User(BaseModel):
    username: str
    password: str
