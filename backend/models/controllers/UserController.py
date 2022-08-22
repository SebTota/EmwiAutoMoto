from fireo.models import Model
from fireo.fields import TextField


class UserController(Model):
    username: str = TextField()
    salt: str = TextField()
    password: str = TextField()
