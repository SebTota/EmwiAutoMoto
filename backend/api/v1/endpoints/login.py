from typing import Any, Optional
from sqlalchemy.orm import Session
from backend.db.init_db import get_db

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from backend import crud, models, schemas
from backend.core import security
from backend.core.logging import logger

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    logger.info(f"User {form_data.username} is attempting to log in.")
    user: Optional[models.User] = crud.user.get_by_email(db, form_data.username)
    if not user or not security.validate_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect user credentials or user doesn't exist")

    return security.create_auth_token(user=user)
