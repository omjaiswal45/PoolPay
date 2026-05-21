from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.pool_member import PoolMember
from decimal import Decimal


class MemberRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db, PoolMember)

    def get_by_pool_id(self, pool_id: str):
        return self.db.query(PoolMember)\
            .filter(PoolMember.pool_id == pool_id)\
            .all()

    def get_by_pool_and_user(self, pool_id: str, user_id: str):
        return self.db.query(PoolMember)\
            .filter(
                PoolMember.pool_id == pool_id,
                PoolMember.user_id == user_id
            )\
            .first()

    def update_total_spent(self, pool_id: str, user_id: str, amount: Decimal):
        member = self.get_by_pool_and_user(pool_id, user_id)
        if not member:
            return None
        member.total_spent += amount
        self.db.commit()
        self.db.refresh(member)
        return member

    def update_contributed_amount(self, pool_id: str, user_id: str, amount: Decimal):
        member = self.get_by_pool_and_user(pool_id, user_id)
        if not member:
            return None
        member.contributed_amount += amount
        self.db.commit()
        self.db.refresh(member)
        return member

    def check_spending_limit(self, pool_id: str, user_id: str, amount: Decimal) -> bool:
        member = self.get_by_pool_and_user(pool_id, user_id)
        if not member:
            return False
        if member.spending_limit is None:
            return True
        return amount <= member.spending_limit