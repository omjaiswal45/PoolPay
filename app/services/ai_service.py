from app.ai.base_provider import BaseAIProvider


class AIService:

    def __init__(self, ai_provider: BaseAIProvider):
        self.ai_provider = ai_provider

    def categorize_expense(self, note: str) -> str:
        if not note:
            return "uncategorized"
        return self.ai_provider.categorize_expense(note)

    def generate_monthly_summary(self, transactions: list) -> str:
        if not transactions:
            return "No transactions found for this period"
        return self.ai_provider.generate_summary(transactions)