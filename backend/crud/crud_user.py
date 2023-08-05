from typing import Optional

from sqlmodel import Session

from backend.core import security
from backend.models.user import User, UserCreate, UserCreateInternal
from backend.utils import get_random_alphanumeric_string


def get(db: Session, obj_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == obj_id).first()


def create(db: Session, obj: UserCreate) -> User:
    obj_create: UserCreateInternal = UserCreateInternal.from_orm(obj)
    obj_create.hashed_password = security.get_password_hash(obj.password)

    db_obj: User = User.from_orm(obj_create)
    db_obj.id = get_random_alphanumeric_string(12)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

