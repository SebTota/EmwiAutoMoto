from typing import Union

from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from backend.models.controllers import MotorcycleController
from backend.models.api import Motorcycle, UpdateMotorcycle, MotorcycleListResponse

router = APIRouter(tags=["Store"])


@router.get('/motorcycles', response_model=MotorcycleListResponse)
def get_motorcycles(limit: int = 9, show_sold: bool = False, pagination_cursor: str = None):
    motorcycles_controller = MotorcycleController.collection.filter(sold=show_sold)

    if pagination_cursor:
        motorcycles_controller = motorcycles_controller.cursor(pagination_cursor)
    else:
        motorcycles_controller = motorcycles_controller.order('date_created')

    motorcycles_controller = motorcycles_controller.fetch(limit)

    motorcycles = [m.to_dict() for m in motorcycles_controller]
    cursor = motorcycles_controller.cursor

    if len(motorcycles) < limit or len(list(MotorcycleController.collection.cursor(cursor).fetch(1))) == 0:
        cursor = None

    return MotorcycleListResponse(num_items=len(motorcycles),
                                  items=motorcycles,
                                  pagination_cursor=cursor)


@router.get('/motorcycle/{item_id}')
def get_motorcycle(item_id: str):
    motorcycle: Union[MotorcycleController, None] = MotorcycleController.collection.get(f'motorcycle_controller/{item_id}')
    if motorcycle is None:
        raise HTTPException(status_code=404, detail='Invalid motorcycle id.')
    else:
        return Motorcycle.parse_obj(motorcycle.to_dict())


@router.post('/motorcycle', status_code=201, response_description="id of the newly created item")
def new_motorcycle(motorcycle: Motorcycle, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    if not valid_motorcycle(motorcycle):
        return HTTPException(status_code=400, detail='Invalid motorcycle details provided.')

    return MotorcycleController.add_motorcycle(motorcycle).id


@router.post('/motorcycle/{item_id}', status_code=201, response_description="id of the updated item")
def update_motorcycle(item_id: str, motorcycle: UpdateMotorcycle, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return MotorcycleController.update_motorcycle(item_id, motorcycle, motorcycle.__fields_set__).id


@router.delete('/motorcycle/{item_id}')
def delete_motorcycle(item_id: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    # TODO: Delete all images related to the motorcycle being deleted
    MotorcycleController.collection.delete(item_id)
    return "Deleted motorcycle"


def valid_motorcycle(motorcycle: Motorcycle) -> bool:
    """
    Validate that a new motorcycle request provided information within set limits.
    """
    if motorcycle.price <= 0 or motorcycle.odometer <= 0 or motorcycle.year < 1000 or motorcycle.year > 9999:
        return False
    return True
