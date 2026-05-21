from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseResponseSchema


class InviteCreateSchema(BaseModel):
    phone_number: Optional[str] = None

    @validator('phone_number')
    def phone_must_be_valid(cls, v):
        if v is not None:
            if not v.startswith('+'):
                raise ValueError('Phone must start with country code like +91')
            if len(v) < 10:
                raise ValueError('Phone number too short')
        return v


class InviteAcceptSchema(BaseModel):
    token: str

    @validator('token')
    def token_must_not_be_empty(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Token cannot be empty')
        return v


class InviteResponseSchema(BaseResponseSchema):
    pool_id: str
    invited_by: str
    invited_phone: Optional[str] = None
    token: str
    expires_at: datetime
    used: bool