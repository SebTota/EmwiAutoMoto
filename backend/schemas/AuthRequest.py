from pydantic.main import BaseModel


class AuthRequest(BaseModel):
    username: str
    password: str
