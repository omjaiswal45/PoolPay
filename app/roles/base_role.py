from abc import ABC, abstractmethod


class BaseRole(ABC):
    @abstractmethod
    def can_spend(self) -> bool:
        pass

    @abstractmethod
    def can_topup(self) -> bool:
        pass

    @abstractmethod
    def can_manage_members(self) -> bool:
        pass
