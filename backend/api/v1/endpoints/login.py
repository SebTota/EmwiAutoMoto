from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from backend import crud, models, schemas
from backend.core import security

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user: Optional[models.User] = await crud.user.get_by_email(form_data.username)
    if not user or not security.validate_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect user credentials or user doesn't exist")

    return security.create_auth_token(user=user)
