from enum import Enum


class ProductStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    deleted = "deleted"
    draft = "draft"
