from pydantic import BaseModel, validator
from typing import Optional
from decimal import Decimal
from app.schemas.base import BaseResponseSchema


class AddMemberSchema(BaseModel):
    user_id: Optional[str] = None
    phone_number: Optional[str] = None

    @validator('phone_number')
    def phone_must_be_valid(cls, v):
        if v is not None:
            if not v.startswith('+'):
                raise ValueError('Phone must start with country code like +91')
            if len(v) < 10:
                raise ValueError('Phone number too short')
        return v


class ChangeLimitSchema(BaseModel):
    spending_limit: Decimal

    @validator('spending_limit')
    def limit_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Spending limit must be greater than 0')
        return v


class ChangeRoleSchema(BaseModel):
    role: str

    @validator('role')
    def role_must_be_valid(cls, v):
        allowed_roles = ['admin', 'member', 'viewer']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of {allowed_roles}')
        return v


class MemberResponseSchema(BaseResponseSchema):
    pool_id: str
    user_id: str
    role: str
    spending_limit: Optional[Decimal] = None
    contributed_amount: Decimal
    total_spent: Decimal