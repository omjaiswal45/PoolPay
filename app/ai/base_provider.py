from abc import ABC, abstractmethod


class BaseAIProvider(ABC):

    @abstractmethod
    def categorize_expense(self, note: str) -> str:
        pass

    @abstractmethod
    def generate_summary(self, transactions: list) -> str:
        pass