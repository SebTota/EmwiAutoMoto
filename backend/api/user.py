from typing import Any, List
import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from backend import crud, schemas, models
from backend.utils import deps
from backend.schemas import AuthRequest, LoggedInUser
from backend.controllers import UserController
from backend.utils.Auth import Auth

router = APIRouter(tags=["User"])


@router.post('/login', response_model=LoggedInUser)
def login(user: AuthRequest, Authorize: AuthJWT = Depends()):
    if not Auth.verify_user(user):
        # TODO - update this once the UI is completed
        raise HTTPException(status_code=401, detail='Invalid username or password.')

    return LoggedInUser(username=user.username,
                 access_token=Authorize.create_access_token(subject=user.username,
                                                            expires_time=datetime.timedelta(days=7)))


@router.post('/register', response_model=LoggedInUser)
def register(user: AuthRequest, Authorize: AuthJWT = Depends()):
    # Since this is ONLY for admins, we don't want anyone to just create a new account for themselves
    Authorize.jwt_required()

    hashed_pass, salt = Auth.hash_password(user.password)
    hashed_pass: str = hashed_pass
    salt: str = salt

    if UserController.collection.filter(username=user.username).get() is not None:
        raise HTTPException(status_code=400, detail='Username already in use.')

    UserController(username=user.username, password=hashed_pass, salt=salt).save()
    return LoggedInUser(username=user.username,
                        access_token=Authorize.create_access_token(subject=user.username,
                                                                   expires_time=datetime.timedelta(days=7)))


@router.get('/user')
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return {
        'username': Authorize.get_jwt_subject()
    }


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
