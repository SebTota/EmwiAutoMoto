import json
import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from jose import jwt
from passlib.context import CryptContext

from backend.core.config import settings
from backend import models
from backend import schemas
from backend import crud
from backend.utils.deps import get_random_string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_auth_token(db: Session, user: models.User) -> schemas.Token:
    # Generate access token
    access_token_expires: datetime = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": access_token_expires, "sub": str(user.id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    # Generate and store the refresh token in the db
    refresh_token: str = secrets.token_urlsafe(32)
    refresh_token_expires: datetime = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token_to_encode = schemas.RefreshToken(user_id=user.id,
                                                   refresh_token=refresh_token,
                                                   expires=refresh_token_expires)

    encoded_refresh_token = jwt.encode(json.loads(refresh_token_to_encode.json()),
                                       settings.REFRESH_TOKEN_SECRET_KEY,
                                       algorithm=ALGORITHM)

    rt_create: schemas.RefreshTokenCreate = schemas.RefreshTokenCreate(id=get_random_string(12),
                                                                       user_id=user.id,
                                                                       refresh_token=refresh_token,
                                                                       expires=refresh_token_expires)
    crud.refresh_token.create_and_add_to_user(db, user, rt_create)

    return schemas.Token(token_type='bearer',
                         access_token=encoded_jwt,
                         access_token_expires=access_token_expires,
                         refresh_token=encoded_refresh_token,
                         refresh_token_expires=refresh_token_expires)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
