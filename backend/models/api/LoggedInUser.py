from pydantic.main import BaseModel


class LoggedInUser(BaseModel):
    username: str
    access_token: str
