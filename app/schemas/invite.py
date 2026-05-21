from pydantic import BaseModel, EmailStr
from datetime import datetime


class InviteCreateSchema(BaseModel):
    pool_id: int
    email: EmailStr


class InviteResponseSchema(BaseModel):
    id: int
    pool_id: int
    token: str
    email: EmailStr
    accepted: bool
    created_at: datetime

    model_config = {"from_attributes": True}
