import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi_jwt_auth import AuthJWT

from backend.models.api import User, LoggedInUser
from backend.models.controllers import UserController
from backend.utils.Auth import Auth

router = APIRouter(tags=["User"])


@router.post('/login', response_model=LoggedInUser)
def login(user: User, Authorize: AuthJWT = Depends()):
    if not Auth.verify_user(user):
        # TODO - update this once the UI is completed
        return RedirectResponse('/login', status_code=401)

    return LoggedInUser(username=user.username,
                        access_token=Authorize.create_access_token(subject=user.username,
                                                                   expires_time=datetime.timedelta(days=7)))


@router.post('/register', response_model=LoggedInUser)
def register(user: User, Authorize: AuthJWT = Depends()):
    hashed_pass, salt = Auth.hash_password(user.password)
    hashed_pass: str = hashed_pass
    salt: str = salt

    if UserController.collection.filter(username=user.username).get() is not None:
        raise HTTPException(status_code=400, detail='Please enter a username that is not in use.')

    user = UserController(username=user.username, password=hashed_pass, salt=salt)
    user.save()

    return LoggedInUser(username=user.username,
                        access_token=Authorize.create_access_token(subject=user.username,
                                                                   expires_time=datetime.timedelta(days=7)))
