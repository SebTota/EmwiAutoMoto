from typing import Optional

from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(index=True, nullable=False, default=True)
    is_superuser: bool = Field(index=True, nullable=False, default=False)


class User(UserBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)


class UserCreate(SQLModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserCreateInternal(UserCreate):
    hashed_password: Optional[str] = None


class UserRead(SQLModel):
    id: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    is_superuser: bool
