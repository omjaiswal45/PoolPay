from app.ai.base_provider import BaseAIProvider
from app.core.config import settings
from openai import OpenAI


class OpenAIProvider(BaseAIProvider):

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def categorize_expense(self, note: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expense categorizer. Return only one category word like: food, travel, fuel, shopping, entertainment, utilities, medical, other."
                    },
                    {
                        "role": "user",
                        "content": f"Categorize this expense: {note}"
                    }
                ],
                max_tokens=10
            )
            return response.choices[0].message.content.strip().lower()
        except Exception:
            return "uncategorized"

    def generate_summary(self, transactions: list) -> str:
        try:
            transaction_text = "\n".join([
                f"{t.type}: {t.amount} — {t.note or 'no note'}"
                for t in transactions
            ])
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial summarizer. Give a brief 3-4 line summary of spending patterns."
                    },
                    {
                        "role": "user",
                        "content": f"Summarize these transactions:\n{transaction_text}"
                    }
                ],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return "Unable to generate summary at this time"