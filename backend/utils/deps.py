import time
from datetime import datetime
import string
import random
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.core import security
from backend.core.config import settings
from backend.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
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
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_user_from_refresh_token(
        encrypted_refresh_token: str, db: Session = Depends(get_db)
) -> schemas.User:
    try:
        payload = jwt.decode(
            encrypted_refresh_token, settings.REFRESH_TOKEN_SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.RefreshToken(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate refresh token")

    refresh_token = crud.refresh_token.get_by_refresh_token(db, decrypted_refresh_token=token_data.refresh_token)
    if refresh_token:
        crud.refresh_token.delete_by_obj(db, refresh_token)

    if not refresh_token or refresh_token.expires < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired refresh token")

    s = time.time()
    user = crud.user.get(db, id=token_data.user_id)
    print(f'DBQuery - GetUser: {(time.time() - s) * 1000} ms')
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

