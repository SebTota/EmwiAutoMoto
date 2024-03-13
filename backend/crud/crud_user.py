from typing import Optional
from sqlalchemy.orm import Session

from backend.core import security
from backend.models.user import User
from backend import schemas
from backend.utils import get_random_alphanumeric_string


def get(db: Session, obj_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == obj_id).first()


def create(db: Session, obj: schemas.UserCreate) -> User:
    user = User(
        id=get_random_alphanumeric_string(12),
        first_name=obj.first_name,
        last_name=obj.last_name,
        email=obj.email,
        hashed_password=security.get_password_hash(obj.password),
        is_superuser=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()
