from sqlalchemy import Column, String, Boolean

from backend.db.init_db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String(12), primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100), unique=True)
    hashed_password = Column(String(128))
    is_superuser = Column(Boolean, default=False)
