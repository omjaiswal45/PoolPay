from app.roles.base_role import BaseRole


class MemberRole(BaseRole):
    def can_spend(self) -> bool:
        return True

    def can_topup(self) -> bool:
        return False

    def can_manage_members(self) -> bool:
        return False
