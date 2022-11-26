from fireo.models import Model
from fireo.fields import TextField


class UserController(Model):
    username: str = TextField(required=True)
    salt: str = TextField(required=True)
    password: str = TextField(required=True)
