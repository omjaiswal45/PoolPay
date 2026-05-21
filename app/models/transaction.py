import uuid
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.dependencies import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pool_id = Column(UUID(as_uuid=True), ForeignKey("pools.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    note = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    receipt_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())