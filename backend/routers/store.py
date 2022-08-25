from typing import Union

from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from backend.models.controllers import MotorcycleController
from backend.models.api import Motorcycle, MotorcycleListResponse

router = APIRouter(tags=["Store"])


@router.get('/motorcycles', response_model=MotorcycleListResponse)
def get_motorcycles(limit: int = 3, show_sold: bool = False, pagination_cursor: str = None):
    motorcycles_controller = MotorcycleController.collection
    if not show_sold:
        motorcycles_controller = motorcycles_controller.filter(sold=False)
    motorcycles_controller = motorcycles_controller.fetch(limit)

    motorcycles = list(motorcycles_controller)
    for i, v in enumerate(motorcycles):
        motorcycles[i] = Motorcycle.parse_obj(v.to_dict())
    return MotorcycleListResponse(num_items=len(motorcycles),
                                  items=motorcycles,
                                  pagination_cursor=None)


@router.get('/motorcycle/{item_id}')
def get_motorcycle(item_id: str):
    motorcycle: Union[MotorcycleController, None] = MotorcycleController.collection.get(f'motorcycle_controller/{item_id}')
    if motorcycle is None:
        raise HTTPException(status_code=404, detail='Invalid motorcycle id.')
    else:
        return Motorcycle.parse_obj(motorcycle.to_dict())


@router.post('/motorcycle')
def new_motorcycle(motorcycle: Motorcycle, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    if not valid_motorcycle(motorcycle):
        return HTTPException(status_code=400, detail='Invalid motorcycle details provided.')
    m: MotorcycleController = MotorcycleController.from_dict(motorcycle.dict(exclude={'key', 'id'}))

    if motorcycle.id:
        m.update(f'motorcycle_controller/{motorcycle.id}')
        return 'Updated existing motorcycle'
    else:
        m.save()
        return 'Added new motorcycle'


@router.delete('/motorcycle')
def delete_motorcycle(key: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    # TODO: Delete all images related to the motorcycle being deleted
    MotorcycleController.collection.delete(key)
    return "Deleted motorcycle"


def valid_motorcycle(motorcycle: Motorcycle) -> bool:
    """
    Validate that a new motorcycle request provided information within set limits.
    """
    if motorcycle.price <= 0 or motorcycle.km <= 0 or motorcycle.year < 1000 or motorcycle.year > 9999:
        return False
    return True
