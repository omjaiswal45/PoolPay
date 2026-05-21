from pydantic import BaseModel, validator
from typing import Optional
from decimal import Decimal
from app.schemas.base import BaseResponseSchema


class PoolCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Pool name cannot be empty')
        if len(v) > 50:
            raise ValueError('Pool name cannot exceed 50 characters')
        return v


class PoolUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None


class PoolResponseSchema(BaseResponseSchema):
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None
    balance: Decimal
    created_by: str


class PoolDetailResponseSchema(PoolResponseSchema):
    total_members: Optional[int] = None
    total_transactions: Optional[int] = None