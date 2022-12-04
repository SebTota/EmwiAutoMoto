from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend import models
from backend.crud.base import CRUDBase
from backend.models.refresh_token import RefreshToken
from backend.schemas.token import RefreshTokenCreate, RefreshTokenUpdate
from backend.utils.deps import get_random_string


class CRUDRefreshToken(CRUDBase[RefreshToken, RefreshTokenCreate, RefreshTokenUpdate]):
    def create(self, db: Session, *, obj_in: RefreshTokenCreate) -> RefreshToken:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, id=get_random_string(12))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_and_add_to_user(
            self, db: Session, db_obj: models.User, obj_in: RefreshTokenCreate
    ) -> RefreshToken:
        """
        db: Database Session
        db_obj: User Database Object
        obj_in: RefreshTokenCreate Object
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_refresh_token(self, db: Session, decrypted_refresh_token: str) -> RefreshToken:
        return db.query(RefreshToken).filter(RefreshToken.refresh_token == decrypted_refresh_token).first()

    def delete_by_obj(self, db: Session, db_obj: models.RefreshToken):
        db.delete(db_obj)
        db.commit()


refresh_token = CRUDRefreshToken(RefreshToken)
