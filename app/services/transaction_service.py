from sqlalchemy.orm import Session
from decimal import Decimal
from fastapi import HTTPException
from app.repositories.pool_repository import PoolRepository
from app.repositories.member_repository import MemberRepository
from app.repositories.transaction_repository import TransactionRepository
from app.services.audit_service import AuditService


class TransactionService:

    def __init__(self, db: Session):
        self.pool_repo = PoolRepository(db)
        self.member_repo = MemberRepository(db)
        self.transaction_repo = TransactionRepository(db)
        self.audit_service = AuditService(db)

    def validate_spend(self, pool_id: str, user_id: str, amount: Decimal):
        member = self.member_repo.get_by_pool_and_user(pool_id, user_id)
        if not member:
            raise HTTPException(status_code=404, detail="You are not a member of this pool")
        if member.role == "viewer":
            raise HTTPException(status_code=403, detail="Viewers cannot spend money")
        pool = self.pool_repo.get_by_id(pool_id)
        if not pool:
            raise HTTPException(status_code=404, detail="Pool not found")
        if pool.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient pool balance")
        limit_ok = self.member_repo.check_spending_limit(pool_id, user_id, amount)
        if not limit_ok:
            raise HTTPException(status_code=400, detail="Amount exceeds your spending limit")
        return member, pool

    def spend_money(self, pool_id: str, user_id: str, amount: Decimal, note: str, category: str = None, receipt_url: str = None):
        member, pool = self.validate_spend(pool_id, user_id, amount)
        transaction = self.transaction_repo.create({
            "pool_id": pool_id,
            "user_id": user_id,
            "type": "expense",
            "amount": amount,
            "note": note,
            "category": category,
            "receipt_url": receipt_url
        })
        new_balance = pool.balance - amount
        self.pool_repo.update_balance(pool_id, new_balance)
        self.member_repo.update_total_spent(pool_id, user_id, amount)
        self.audit_service.log_expense(
            pool_id=pool_id,
            user_id=user_id,
            amount=str(amount),
            note=note
        )
        return transaction

    def topup_money(self, pool_id: str, user_id: str, amount: Decimal, note: str = None):
        member = self.member_repo.get_by_pool_and_user(pool_id, user_id)
        if not member:
            raise HTTPException(status_code=404, detail="You are not a member of this pool")
        pool = self.pool_repo.get_by_id(pool_id)
        if not pool:
            raise HTTPException(status_code=404, detail="Pool not found")
        transaction = self.transaction_repo.create({
            "pool_id": pool_id,
            "user_id": user_id,
            "type": "topup",
            "amount": amount,
            "note": note
        })
        new_balance = pool.balance + amount
        self.pool_repo.update_balance(pool_id, new_balance)
        self.member_repo.update_contributed_amount(pool_id, user_id, amount)
        self.audit_service.log_topup(
            pool_id=pool_id,
            user_id=user_id,
            amount=str(amount)
        )
        return transaction

    def get_transaction_history(self, pool_id: str):
        return self.transaction_repo.get_by_pool_id(pool_id)

    def get_transaction_by_id(self, transaction_id: str):
        transaction = self.transaction_repo.get_by_id(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction

    def get_spending_summary(self, pool_id: str):
        return self.transaction_repo.get_spending_by_member(pool_id)

    def get_topup_summary(self, pool_id: str):
        return self.transaction_repo.get_total_expense_by_pool(pool_id)