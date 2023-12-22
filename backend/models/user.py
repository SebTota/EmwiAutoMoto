from tortoise import fields, models


class User(models.Model):
    id: str = fields.CharField(max_length=12, pk=True)
    first_name: str = fields.CharField(max_length=100)
    last_name: str = fields.CharField(max_length=100)
    email: str = fields.CharField(max_length=100, unique=True)
    hashed_password: str = fields.CharField(max_length=128)
    is_superuser: bool = fields.BooleanField(default=False)
