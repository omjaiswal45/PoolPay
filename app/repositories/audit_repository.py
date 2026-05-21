from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.audit_log import AuditLog


class AuditRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db, AuditLog)

    def get_by_pool_id(self, pool_id: str):
        return self.db.query(AuditLog)\
            .filter(AuditLog.pool_id == pool_id)\
            .order_by(AuditLog.created_at.desc())\
            .all()

    def get_by_user_id(self, user_id: str):
        return self.db.query(AuditLog)\
            .filter(AuditLog.user_id == user_id)\
            .order_by(AuditLog.created_at.desc())\
            .all()

    def get_by_action(self, pool_id: str, action: str):
        return self.db.query(AuditLog)\
            .filter(
                AuditLog.pool_id == pool_id,
                AuditLog.action == action
            )\
            .order_by(AuditLog.created_at.desc())\
            .all()