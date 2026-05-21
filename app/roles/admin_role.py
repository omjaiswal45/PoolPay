from app.roles.base_role import BaseRole


class AdminRole(BaseRole):
    def can_spend(self) -> bool:
        return True

    def can_topup(self) -> bool:
        return True

    def can_manage_members(self) -> bool:
        return True
