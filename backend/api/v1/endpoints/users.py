from typing import Any, Optional
from sqlalchemy.orm import Session
from backend.db.init_db import get_db

from fastapi import APIRouter, Depends, HTTPException

from backend import crud, models, schemas
from backend.utils import deps

router = APIRouter()


@router.post("", response_model=schemas.UserRead)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user: Optional[models.User] = crud.user.get_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email or username already exists in the system.",
        )
    user = crud.user.create(db, user_in)
    return user


@router.get("/me", response_model=schemas.UserRead)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
