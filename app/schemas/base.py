from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BaseResponseSchema(BaseModel):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class BasePaginationSchema(BaseModel):
    page: int = 1
    limit: int = 10