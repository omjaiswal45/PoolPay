import uuid
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.dependencies import Base

class PoolMember(Base):
    __tablename__ = "pool_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pool_id = Column(UUID(as_uuid=True), ForeignKey("pools.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False, default="member")
    spending_limit = Column(Numeric(10, 2), nullable=True)
    contributed_amount = Column(Numeric(10, 2), default=0)
    total_spent = Column(Numeric(10, 2), default=0)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())