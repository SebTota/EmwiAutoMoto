import datetime
import logging
import string
import random
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.core import security
from backend.core.config import settings
from backend.db.init_db import get_db

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

reusable_oauth2_no_error = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    auto_error=False
)


def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def get_current_user_if_signed_in(
        db: Session = Depends(get_db),
        token: str = Depends(reusable_oauth2_no_error)
) -> Optional[models.User]:
    start_time = datetime.datetime.now()
    if not token:
        logging.info(f"No token. Get current user check took {(datetime.datetime.now() - start_time).total_seconds()} seconds")
        return None

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        logging.info(f"No JWT. Get current user check took {(datetime.datetime.now() - start_time).total_seconds()} seconds")
        return None

    user = crud.user.get(db, token_data.sub)

    logging.info(f"Get current user check took {(datetime.datetime.now() - start_time).total_seconds()} seconds")
    if not user:
        return None
    return user


def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="Could not authenticate user. User not found")

    logging.info(f"Logged in user: {user.email}")
    return user


def get_current_active_superuser(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_active_superuser_no_exception(
        current_user: models.User = Depends(get_current_user_if_signed_in),
) -> Optional[models.User]:
    if not current_user or not current_user.is_superuser:
        return None
    return current_user