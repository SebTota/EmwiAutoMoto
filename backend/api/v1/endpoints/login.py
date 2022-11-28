from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.utils import deps
from backend.core import security

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    return security.create_auth_token(db=db, user=user)


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/login/refresh-token", response_model=schemas.Token)
def refresh_access_token(refresh_token_request: schemas.TokenRefreshRequest, db: Session = Depends(deps.get_db)) -> Any:
    """
    Refresh access token.
    """
    user = crud.user.get_by_username(db=db, username=refresh_token_request.username)
    if not user:
        # Do not give error specific to username being invalid to avoid username guessing abuse
        raise HTTPException(status_code=400, detail="Invalid refresh credentials")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    if security.verify_refresh_token_valid(user, refresh_token_request.refresh_token):
        return security.create_auth_token(db=db, user=user)
    else:
        raise HTTPException(status_code=400, detail="Invalid refresh credentials")
