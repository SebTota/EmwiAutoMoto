from backend.models import Product

from tortoise import fields


class VehicleBase(Product):
    year = fields.IntField()
    make = fields.CharField(max_length=100)
    model = fields.CharField(max_length=100)
    vin = fields.CharField(max_length=100, null=True)
    odometer = fields.IntField()
    color = fields.CharField(max_length=100)