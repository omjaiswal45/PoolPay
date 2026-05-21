from pydantic import BaseModel, validator
from typing import Optional
from decimal import Decimal
from app.schemas.base import BaseResponseSchema, BasePaginationSchema


class TopupSchema(BaseModel):
    amount: Decimal
    note: Optional[str] = None

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        if v > 100000:
            raise ValueError('Amount cannot exceed 100000')
        return v


class ExpenseSchema(BaseModel):
    amount: Decimal
    note: Optional[str] = None
    category: Optional[str] = None
    receipt_url: Optional[str] = None

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        if v > 100000:
            raise ValueError('Amount cannot exceed 100000')
        return v

    @validator('note')
    def note_must_not_be_empty(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('Note cannot be empty')
        return v


class TransactionResponseSchema(BaseResponseSchema):
    pool_id: str
    user_id: str
    type: str
    amount: Decimal
    note: Optional[str] = None
    category: Optional[str] = None
    receipt_url: Optional[str] = None


class TransactionFilterSchema(BasePaginationSchema):
    type: Optional[str] = None
    category: Optional[str] = None