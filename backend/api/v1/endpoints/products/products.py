from abc import ABC
from typing import Any, List, Optional
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.db.init_db import get_db
from backend.models import User, ProductStatus
from backend.utils import deps


class AbstractProductAPI(ABC):

    @classmethod
    def setup_routes(cls, crud_class, product_model, schema_product_create,
                     schema_product_read_no_media, schema_product_read_with_media,
                     schema_product_list):
        router = APIRouter()

        @router.get("", response_model=schema_product_list)
        def read_items(
                show_status: List[ProductStatus] = Query([ProductStatus.FOR_SALE]),
                page: int = 1,
                limit: int = 12,
                db: Session = Depends(get_db),
                current_user: User = Depends(deps.get_current_active_superuser_no_exception),
        ) -> Any:
            """
            Retrieve products with specified filters.
            """

            if page < 1:
                raise HTTPException(status_code=400, detail="Page must be greater than 0")

            if limit < 1:
                raise HTTPException(status_code=400, detail="Limit must be greater than 0")

            if ProductStatus.DELETED in show_status or ProductStatus.DRAFT in show_status:
                if not current_user or not current_user.is_superuser:
                    raise HTTPException(status_code=403, detail="You must be a superuser to view these items")

            offset: int = (page - 1) * limit

            # Add 1 to the limit to see if there is a next page.
            items: List[schema_product_read_no_media] = (
                crud_class.get_multi_with_filters(db,
                                                  offset,
                                                  limit + 1,
                                                  show_status))

            if not items:
                return schema_product_list(page=page,
                                           has_next_page=False,
                                           products=[])

            has_next_page = True if len(items) > limit else False

            # Remove the extra products we got as a pagination test IFF there is a next page
            # (indicating we received +1 results back from db)
            if has_next_page:
                items.pop()

            return schema_product_list(page=page,
                                       has_next_page=has_next_page,
                                       products=items)

        @router.post("", response_model=schema_product_read_with_media)
        def create_item(
                item_in: schema_product_create,
                db: Session = Depends(get_db),
                current_user: User = Depends(deps.get_current_active_superuser),
        ) -> Any:
            """
            Create new product.
            """
            return crud_class.create(db, item_in)

        @router.put("/{id}", response_model=schema_product_read_with_media)
        def update_item(
                id: str,
                item_in: schema_product_create,
                db: Session = Depends(get_db),
                current_user: User = Depends(deps.get_current_active_superuser),
        ) -> Any:
            """
            Update a product.
            """
            item: Optional[product_model] = crud_class.get(db, id)
            if not item:
                raise HTTPException(status_code=404, detail="No product found with this id.")
            item = crud_class.update(db, item, item_in)
            return item

        @router.get("/{id}", response_model=schema_product_read_with_media)
        def read_item(
                id: str,
                db: Session = Depends(get_db),
                current_user: User = Depends(deps.get_current_active_superuser_no_exception),
        ) -> Any:
            """
            Get item by ID.
            """
            item = crud_class.get_with_media(db, id)

            if not item:
                raise HTTPException(status_code=404, detail="No product found with this ID")

            if item.status in [ProductStatus.DRAFT, ProductStatus.DELETED]:
                if not current_user or not current_user.is_superuser:
                    raise HTTPException(status_code=403, detail="You must be a superuser to view this item")

            return item

        return router
