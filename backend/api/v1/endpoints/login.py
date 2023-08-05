from typing import Any, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend import crud, models
from backend.utils import deps
from backend.core import security

router = APIRouter()


@router.post("/login/access-token", response_model=models.Token)
def login_access_token(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user: Optional[models.User] = crud.user.get_by_email(db, form_data.username)
    if not user or not security.validate_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect user credentials or user doesn't exist")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return security.create_auth_token(db=db, user=user)


# @router.post("/login/refresh-token", response_model=models.Token)
# def refresh_access_token(refresh_token_request: schemas.TokenRefreshRequest, db: Session = Depends(deps.get_db)) -> Any:
#     """
#     Refresh access token.
#     """
#     user = crud.user.get_by_username(db=db, username=refresh_token_request.username)
#     if not user:
#         # Do not give error specific to username being invalid to avoid username guessing abuse
#         raise HTTPException(status_code=400, detail="Invalid refresh credentials")
#     elif not crud.user.is_active(user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#
#     if security.verify_refresh_token_valid(user, refresh_token_request.refresh_token):
#         return security.create_auth_token(db=db, user=user)
#     else:
#         raise HTTPException(status_code=400, detail="Invalid refresh credentials")
