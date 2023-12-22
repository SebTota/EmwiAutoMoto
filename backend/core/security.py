from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from backend.core.config import settings
from backend import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_auth_token(user: models.User) -> schemas.Token:
    # Generate access token
    access_token_expires: datetime = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": access_token_expires, "sub": str(user.id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return schemas.Token(token_type='bearer',
                         access_token=encoded_jwt,
                         access_token_expires=access_token_expires)


def validate_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
