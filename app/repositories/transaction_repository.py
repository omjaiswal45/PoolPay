from sqlalchemy.orm import Session
from sqlalchemy import func
from app.repositories.base_repository import BaseRepository
from app.models.transaction import Transaction
from decimal import Decimal


class TransactionRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db, Transaction)

    def get_by_pool_id(self, pool_id: str):
        return self.db.query(Transaction)\
            .filter(Transaction.pool_id == pool_id)\
            .order_by(Transaction.created_at.desc())\
            .all()

    def get_by_user_and_pool(self, pool_id: str, user_id: str):
        return self.db.query(Transaction)\
            .filter(
                Transaction.pool_id == pool_id,
                Transaction.user_id == user_id
            )\
            .order_by(Transaction.created_at.desc())\
            .all()

    def get_total_expense_by_pool(self, pool_id: str) -> Decimal:
        result = self.db.query(func.sum(Transaction.amount))\
            .filter(
                Transaction.pool_id == pool_id,
                Transaction.type == "expense"
            )\
            .scalar()
        return result or Decimal('0')

    def get_total_by_user_and_pool(self, pool_id: str, user_id: str, type: str) -> Decimal:
        result = self.db.query(func.sum(Transaction.amount))\
            .filter(
                Transaction.pool_id == pool_id,
                Transaction.user_id == user_id,
                Transaction.type == type
            )\
            .scalar()
        return result or Decimal('0')

    def get_by_category(self, pool_id: str, category: str):
        return self.db.query(Transaction)\
            .filter(
                Transaction.pool_id == pool_id,
                Transaction.category == category
            )\
            .all()

    def get_spending_by_member(self, pool_id: str):
        return self.db.query(
                Transaction.user_id,
                func.sum(Transaction.amount).label('total')
            )\
            .filter(
                Transaction.pool_id == pool_id,
                Transaction.type == "expense"
            )\
            .group_by(Transaction.user_id)\
            .all()