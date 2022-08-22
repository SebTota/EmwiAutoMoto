import bcrypt

from backend.models.api import User
from backend.models.controllers import UserController


class Auth:
    @staticmethod
    def verify_user(user: User) -> bool:
        db_user: UserController = UserController.collection.filter(username=user.username).get()

        if db_user is None:
            return False

        return Auth.verify_password(user.password, db_user.salt, db_user.password)

    @staticmethod
    def verify_password(password: str, salt: str, hashed_password: str) -> bool:
        temp_hash: bytes = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))
        return type(temp_hash) == type(hashed_password.encode('utf-8')) and temp_hash == hashed_password.encode('utf-8')

    @staticmethod
    def hash_password(password: str) -> (str, str):
        """
        Hash the given password.

        @returns
        (hashed_password: str, salt: str)
        """
        salt: bytes = bcrypt.gensalt()
        hashed_password: bytes = bcrypt.hashpw(str.encode(password), salt)
        return hashed_password.decode('utf-8'), salt.decode('utf-8')
