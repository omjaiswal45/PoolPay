from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException
import secrets
from app.repositories.invite_repository import InviteRepository
from app.repositories.member_repository import MemberRepository
from app.repositories.user_repository import UserRepository
from app.services.audit_service import AuditService


class InviteService:

    def __init__(self, db: Session):
        self.invite_repo = InviteRepository(db)
        self.member_repo = MemberRepository(db)
        self.user_repo = UserRepository(db)
        self.audit_service = AuditService(db)

    def generate_token(self) -> str:
        return secrets.token_urlsafe(32)

    def create_invite(self, pool_id: str, invited_by: str, phone_number: str = None):
        token = self.generate_token()
        expires_at = datetime.utcnow() + timedelta(days=7)
        invite = self.invite_repo.create({
            "pool_id": pool_id,
            "invited_by": invited_by,
            "invited_phone": phone_number,
            "token": token,
            "expires_at": expires_at,
            "used": False
        })
        self.audit_service.log_member_added(
            pool_id=pool_id,
            user_id=invited_by,
            member_name=phone_number or "unknown"
        )
        return invite

    def validate_token(self, token: str):
        invite = self.invite_repo.get_by_token(token)
        if not invite:
            raise HTTPException(status_code=404, detail="Invite not found")
        if invite.used:
            raise HTTPException(status_code=400, detail="Invite already used")
        if invite.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Invite has expired")
        return invite

    def accept_invite(self, token: str, user_id: str):
        invite = self.validate_token(token)
        existing = self.member_repo.get_by_pool_and_user(
            str(invite.pool_id),
            user_id
        )
        if existing:
            raise HTTPException(status_code=400, detail="You are already a member of this pool")
        member = self.member_repo.create({
            "pool_id": str(invite.pool_id),
            "user_id": user_id,
            "role": "member",
            "contributed_amount": 0,
            "total_spent": 0
        })
        self.invite_repo.mark_as_used(token)
        self.audit_service.log_member_added(
            pool_id=str(invite.pool_id),
            user_id=user_id,
            member_name=user_id
        )
        return member

    def invite_by_phone(self, pool_id: str, invited_by: str, phone_number: str):
        user = self.user_repo.get_by_phone(phone_number)
        if user:
            existing = self.member_repo.get_by_pool_and_user(
                pool_id,
                str(user.id)
            )
            if existing:
                raise HTTPException(status_code=400, detail="User already in pool")
            member = self.member_repo.create({
                "pool_id": pool_id,
                "user_id": str(user.id),
                "role": "member",
                "contributed_amount": 0,
                "total_spent": 0
            })
            self.audit_service.log_member_added(
                pool_id=pool_id,
                user_id=invited_by,
                member_name=phone_number
            )
            return {"status": "added", "member": member}
        else:
            invite = self.create_invite(pool_id, invited_by, phone_number)
            return {"status": "invited", "token": invite.token}