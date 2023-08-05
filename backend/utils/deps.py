import string
import random
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend import crud, models
from backend.core import security
from backend.core.config import settings
from backend.db.session import engine

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

reusable_oauth2_no_error = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    auto_error=False
)


def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def get_db() -> Generator:
    with Session(engine) as session:
        yield session


def get_current_user_if_signed_in(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2_no_error)
) -> Optional[models.User]:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = models.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        return None
    user = crud.user.get(db, token_data.sub)
    if not user:
        return None
    return user


def get_current_active_superuser_if_signed_in(
    current_user: models.User = Depends(get_current_user_if_signed_in),
) -> Optional[models.User]:
    if not current_user or not current_user.is_superuser:
        return None
    return current_user


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = models.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

