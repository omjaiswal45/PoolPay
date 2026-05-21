from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from app.schemas.base import BaseResponseSchema


class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    password: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        return v

    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

    @validator('phone_number')
    def phone_must_be_valid(cls, v):
        if v is not None:
            if not v.startswith('+'):
                raise ValueError('Phone must start with country code like +91')
            if len(v) < 10:
                raise ValueError('Phone number too short')
        return v


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseResponseSchema):
    name: str
    email: str
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None