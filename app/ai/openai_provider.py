from app.ai.base_provider import BaseAIProvider


class OpenAIProvider(BaseAIProvider):
    async def complete(self, prompt: str) -> str:
        raise NotImplementedError
