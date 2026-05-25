from sqlalchemy.orm import Session
from app.repositories.audit_repository import AuditRepository


class AuditService:

    def __init__(self, db: Session):
        self.audit_repo = AuditRepository(db)

    def log_pool_created(self, pool_id: str, user_id: str, pool_name: str):
        return self.audit_repo.create({
            "pool_id": pool_id,
            "user_id": user_id,
            "action": "pool_created",
            "detail": f"Pool '{pool_name}' was created"
        })

    def log_member_added(self, pool_id: str, user_id: str, member_name: str):
        return self.audit_repo.create({
            "pool_id": pool_id,
            "user_id": user_id,
            "action": "member_added",
            "detail": f"{member_name} was added to pool"
        })

    def log_member_removed(self, pool_id: str, user_id: str, member_name: str):
        return self.audit_repo.create({
            "pool_id": pool_id,
            "user_id": user_id,
            "action": "member_removed",
            "detail": f"{member_name} was removed from pool"
        })

    def log_expense(self, pool_id: str, user_id: str, amount: str, note: str):
        return self.audit_repo.create({
            "pool_id": pool_id,
            "user_id": user_id,
            "action": "expense_logged",
            "detail": f"Spent {amount} — {note}"
        })

    def log_topup(self, pool_id: str, user_id: str, amount: str):
        return self.audit_repo.create({
            "pool_id": pool_id,
            "user_id": user_id,
            "action": "topup_done",
            "detail": f"Added {amount} to pool"
        })

    def log_role_changed(self, pool_id: str, user_id: str, member_name: str, new_role: str):
        return self.audit_repo.create({
            "pool_id": pool_id,
            "user_id": user_id,
            "action": "role_changed",
            "detail": f"{member_name} role changed to {new_role}"
        })

    def log_limit_changed(self, pool_id: str, user_id: str, member_name: str, new_limit: str):
        return self.audit_repo.create({
            "pool_id": pool_id,
            "user_id": user_id,
            "action": "limit_changed",
            "detail": f"{member_name} spending limit changed to {new_limit}"
        })

    def get_pool_audit_history(self, pool_id: str):
        return self.audit_repo.get_by_pool_id(pool_id)

    def get_user_audit_history(self, user_id: str):
        return self.audit_repo.get_by_user_id(user_id)