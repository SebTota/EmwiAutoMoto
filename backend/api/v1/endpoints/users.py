from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException

from backend import crud, models, schemas
from backend.utils import deps

router = APIRouter()


@router.post("", response_model=schemas.UserRead)
async def create_user(
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user: Optional[models.User] = await crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email or username already exists in the system.",
        )
    user = await crud.user.create(user_in)
    return user


@router.get("/me", response_model=schemas.UserRead)
async def read_user_me(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
