from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class MemberResponseSchema(BaseModel):
    id: int
    pool_id: int
    user_id: int
    role: str

    model_config = {"from_attributes": True}


class ChangeLimitSchema(BaseModel):
    spend_limit: Optional[Decimal] = None
