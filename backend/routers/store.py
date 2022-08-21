from fastapi import APIRouter, HTTPException
from backend.models.controllers import MotorcycleController
from backend.models.api import Motorcycle, MotorcycleListResponse

router = APIRouter(tags=["Store"])


@router.get('/motorcycles', response_model=MotorcycleListResponse)
def get_motorcycles(limit: int = 3, show_sold: bool = False, pagination_cursor: str = None):
    motorcycles_controller = motorcycles = MotorcycleController.collection
    if not show_sold:
        motorcycles_controller = motorcycles_controller.filter(sold=False)
    motorcycles_controller = motorcycles_controller.fetch(limit)

    motorcycles = list(motorcycles_controller)
    for i, v in enumerate(motorcycles):
        motorcycles[i] = Motorcycle.parse_obj(v.to_dict())
    return MotorcycleListResponse(num_items=len(motorcycles),
                                  items=motorcycles,
                                  pagination_cursor=None)


@router.post('/motorcycle')
def new_motorcycle(motorcycle: Motorcycle):
    if not valid_motorcycle(motorcycle):
        return HTTPException(status_code=400, detail='Invalid motorcycle details provided.')
    m: MotorcycleController = MotorcycleController.from_dict(motorcycle.dict())
    m.save()
    return "OK"


def valid_motorcycle(motorcycle: Motorcycle) -> bool:
    """
    Validate that a new motorcycle request provided information within set limits.
    """
    if motorcycle.price <= 0 or motorcycle.km <= 0 or motorcycle.year < 1000 or motorcycle.year > 9999:
        return False

