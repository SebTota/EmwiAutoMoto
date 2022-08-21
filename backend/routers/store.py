from fastapi import APIRouter
from backend.models import Motorcycle

router = APIRouter(tags=["Store"])


@router.get('/items')
def items(show_sold: bool = False, pagination_start: int = 0):
    return Motorcycle(year='test')


@router.post('/item')
def addItem():
    m: Motorcycle = Motorcycle(year=2000, make='Subaru', model='Somemodel',
                               km=5000, color='White', price=13500, description='Super nice motorcycle',
                               sold=False, images=[], videos=[])
    m.save()
    return m.key
