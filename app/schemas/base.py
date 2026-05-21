from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")


class BaseResponseSchema(BaseModel):
    success: bool = True
    message: str = "OK"


class BasePaginationSchema(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
