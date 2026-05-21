from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional


class TopupSchema(BaseModel):
    pool_id: int
    amount: Decimal
    description: Optional[str] = None


class ExpenseSchema(BaseModel):
    pool_id: int
    amount: Decimal
    description: Optional[str] = None


class TransactionResponseSchema(BaseModel):
    id: int
    pool_id: int
    user_id: int
    amount: Decimal
    type: str
    description: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
