from pydantic import BaseModel
from decimal import Decimal


class PoolCreateSchema(BaseModel):
    name: str


class PoolResponseSchema(BaseModel):
    id: int
    name: str
    balance: Decimal
    owner_id: int

    model_config = {"from_attributes": True}
