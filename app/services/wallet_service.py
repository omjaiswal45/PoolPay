from sqlalchemy.orm import Session
from app.repositories.pool_repository import PoolRepository
from app.repositories.member_repository import MemberRepository
from app.services.audit_service import AuditService
from fastapi import HTTPException


class WalletService:

    def __init__(self, db: Session):
        self.pool_repo = PoolRepository(db)
        self.member_repo = MemberRepository(db)
        self.audit_service = AuditService(db)

    def create_pool(self, name: str, description: str, icon_url: str, created_by: str):
        pool = self.pool_repo.create({
            "name": name,
            "description": description,
            "icon_url": icon_url,
            "balance": 0,
            "created_by": created_by
        })
        self.member_repo.create({
            "pool_id": str(pool.id),
            "user_id": created_by,
            "role": "admin",
            "contributed_amount": 0,
            "total_spent": 0
        })
        self.audit_service.log_pool_created(
            pool_id=str(pool.id),
            user_id=created_by,
            pool_name=name
        )
        return pool

    def get_pool_details(self, pool_id: str):
        pool = self.pool_repo.get_by_id(pool_id)
        if not pool:
            raise HTTPException(status_code=404, detail="Pool not found")
        return pool

    def get_balance(self, pool_id: str):
        pool = self.pool_repo.get_by_id(pool_id)
        if not pool:
            raise HTTPException(status_code=404, detail="Pool not found")
        return pool.balance

    def add_member(self, pool_id: str, user_id: str, added_by: str, member_name: str):
        admin = self.member_repo.get_by_pool_and_user(pool_id, added_by)
        if not admin or admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin can add members")
        existing = self.member_repo.get_by_pool_and_user(pool_id, user_id)
        if existing:
            raise HTTPException(status_code=400, detail="User already in pool")
        member = self.member_repo.create({
            "pool_id": pool_id,
            "user_id": user_id,
            "role": "member",
            "contributed_amount": 0,
            "total_spent": 0
        })
        self.audit_service.log_member_added(
            pool_id=pool_id,
            user_id=added_by,
            member_name=member_name
        )
        return member

    def remove_member(self, pool_id: str, user_id: str, removed_by: str, member_name: str):
        admin = self.member_repo.get_by_pool_and_user(pool_id, removed_by)
        if not admin or admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin can remove members")
        member = self.member_repo.get_by_pool_and_user(pool_id, user_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        self.member_repo.delete(member.id)
        self.audit_service.log_member_removed(
            pool_id=pool_id,
            user_id=removed_by,
            member_name=member_name
        )
        return True

    def change_role(self, pool_id: str, user_id: str, new_role: str, changed_by: str, member_name: str):
        admin = self.member_repo.get_by_pool_and_user(pool_id, changed_by)
        if not admin or admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin can change roles")
        member = self.member_repo.get_by_pool_and_user(pool_id, user_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        updated = self.member_repo.update(member.id, {"role": new_role})
        self.audit_service.log_role_changed(
            pool_id=pool_id,
            user_id=changed_by,
            member_name=member_name,
            new_role=new_role
        )
        return updated

    def change_spending_limit(self, pool_id: str, user_id: str, new_limit: float, changed_by: str, member_name: str):
        admin = self.member_repo.get_by_pool_and_user(pool_id, changed_by)
        if not admin or admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin can change spending limits")
        member = self.member_repo.get_by_pool_and_user(pool_id, user_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        updated = self.member_repo.update(member.id, {"spending_limit": new_limit})
        self.audit_service.log_limit_changed(
            pool_id=pool_id,
            user_id=changed_by,
            member_name=member_name,
            new_limit=str(new_limit)
        )
        return updated

    def delete_pool(self, pool_id: str, deleted_by: str):
        admin = self.member_repo.get_by_pool_and_user(pool_id, deleted_by)
        if not admin or admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin can delete pool")
        self.pool_repo.delete(pool_id)
        return True

    def get_pools_by_user(self, user_id: str):
        return self.member_repo.get_by_pool_id(user_id)