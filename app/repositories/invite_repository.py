from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.invite import Invite


class InviteRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db, Invite)

    def get_by_token(self, token: str):
        return self.db.query(Invite)\
            .filter(Invite.token == token)\
            .first()

    def get_by_phone(self, phone_number: str):
        return self.db.query(Invite)\
            .filter(Invite.invited_phone == phone_number)\
            .all()

    def get_by_pool_id(self, pool_id: str):
        return self.db.query(Invite)\
            .filter(Invite.pool_id == pool_id)\
            .all()

    def mark_as_used(self, token: str):
        invite = self.get_by_token(token)
        if not invite:
            return None
        invite.used = True
        self.db.commit()
        self.db.refresh(invite)
        return invite