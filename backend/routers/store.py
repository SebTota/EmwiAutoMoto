from fastapi import APIRouter
from backend.models.controllers import MotorcycleController
from backend.models.api import Motorcycle, MotorcycleListResponse

router = APIRouter(tags=["Store"])


@router.get('/motorcycles', response_model=MotorcycleListResponse)
def get_motorcycles(limit: int = 3, show_sold: bool = False, pagination_cursor: str = None):
    motorcycles = motorcycles = MotorcycleController.collection
    if not show_sold:
        motorcycles = motorcycles.filter(sold=False)
    motorcycles = motorcycles.fetch(limit)

    l_motorcycles = list(motorcycles)
    for i, v in enumerate(l_motorcycles):
        l_motorcycles[i] = Motorcycle.parse_obj(v.to_dict())
    return MotorcycleListResponse(num_items=len(l_motorcycles),
                                  items=l_motorcycles,
                                  pagination_cursor=None)


@router.post('/motorcycle')
def new_motorcycle(motorcycle: Motorcycle):
    m: MotorcycleController = MotorcycleController.from_dict(motorcycle.dict())
    m.save()
    return m.key
