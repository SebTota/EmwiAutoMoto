import secrets
from datetime import datetime, timedelta
from typing import Any, Union
from sqlalchemy.orm import Session

from jose import jwt
from passlib.context import CryptContext

from backend.core.config import settings
from backend import models
from backend import schemas
from backend import crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_refresh_token() -> str:
    return secrets.token_urlsafe(32)


def create_auth_token(db: Session, user: models.User) -> schemas.Token:
    # Generate access token
    access_token_expires: datetime = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": access_token_expires, "sub": str(user.id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    # Generate and store the refresh token in the db
    refresh_token: str = create_refresh_token()
    refresh_token_expires: datetime = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    user_update: schemas.UserUpdateBackend = schemas.UserUpdateBackend(refresh_token=refresh_token,
                                                                       refresh_token_expires=refresh_token_expires)
    crud.user.update(db, db_obj=user, obj_in=user_update)

    return schemas.Token(token_type='bearer',
                         access_token=encoded_jwt,
                         access_token_expires=access_token_expires,
                         refresh_token=refresh_token,
                         refresh_token_expires=refresh_token_expires)


def verify_refresh_token_valid(user: models.User, refresh_token: str) -> bool:
    return user.refresh_token_expires > datetime.utcnow() and user.refresh_token == refresh_token


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
