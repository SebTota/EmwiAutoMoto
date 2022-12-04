import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    token_type: str
    access_token: str
    access_token_expires: datetime.datetime
    refresh_token: str
    refresh_token_expires: datetime.datetime


class TokenPayload(BaseModel):
    sub: Optional[int] = None


# Request data when trying to refresh auth token using refresh token
class TokenRefreshRequest(BaseModel):
    refresh_token: str
