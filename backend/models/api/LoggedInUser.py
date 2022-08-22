from typing import Union

from pydantic.main import BaseModel


class LoggedInUser(BaseModel):
    username: str
    access_token: Union[str, None]
