from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {"from_attributes": True}
