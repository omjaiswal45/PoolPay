from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.pool import Pool
from decimal import Decimal


class PoolRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db, Pool)

    def get_by_user_id(self, user_id: str):
        return self.db.query(Pool)\
            .filter(Pool.created_by == user_id)\
            .all()

    def update_balance(self, pool_id: str, new_balance: Decimal):
        pool = self.get_by_id(pool_id)
        if not pool:
            return None
        pool.balance = new_balance
        self.db.commit()
        self.db.refresh(pool)
        return pool