from sqlmodel import SQLModel

from backend.db.session import engine
from backend import models  # DO NOT DELETE THIS!


def init_db() -> None:
    print("Creating db connection and init engine...")
    SQLModel.metadata.create_all(engine)
    print("Created db connection...")
