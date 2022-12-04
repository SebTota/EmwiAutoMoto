import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr


# Shared properties
class UserBase(BaseModel):
    first_name: Optional[constr(max_length=20)] = None
    last_name: Optional[constr(max_length=20)] = None
    username: Optional[constr(max_length=20)] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Updated on the user that only the backend can perform
class UserUpdateBackend(UserUpdate):
    refresh_token: Optional[str] = None
    refresh_token_expires: Optional[datetime.datetime] = None


class UserInDBBase(UserBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
    refresh_token: Optional[str] = None
    refresh_token_expires: Optional[datetime.datetime] = None
