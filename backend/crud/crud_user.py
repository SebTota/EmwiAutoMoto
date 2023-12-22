from typing import Optional

from backend.core import security
from backend.models.user import User
from backend import schemas
from backend.utils import get_random_alphanumeric_string


async def get(obj_id: str) -> Optional[User]:
    return await User.filter(id=obj_id).first()


async def create(obj: schemas.UserCreate) -> User:
    return await User.create(id=get_random_alphanumeric_string(12),
                             first_name=obj.first_name,
                             last_name=obj.last_name,
                             email=obj.email,
                             hashed_password=security.get_password_hash(obj.password),
                             is_superuser=False)


async def get_by_email(email: str) -> Optional[User]:
    return await User.filter(email=email).first()
