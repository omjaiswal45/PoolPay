from app.roles.base_role import BaseRole


class ViewerRole(BaseRole):
    def can_spend(self) -> bool:
        return False

    def can_topup(self) -> bool:
        return False

    def can_manage_members(self) -> bool:
        return False
