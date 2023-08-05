<<<<<<< HEAD
from typing import Any, List, Optional
=======
from typing import Any, Optional
>>>>>>> 6e391b258bb8c115b098697b5858fd335f74492f

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import crud, models
<<<<<<< HEAD
from backend.core import security
=======
>>>>>>> 6e391b258bb8c115b098697b5858fd335f74492f
from backend.utils import deps

router = APIRouter()


@router.post("/", response_model=models.UserRead)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: models.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user: Optional[models.User] = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email or username already exists in the system.",
        )
    user = crud.user.create(db, user_in)
    return user


@router.get("/me", response_model=models.UserRead)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
