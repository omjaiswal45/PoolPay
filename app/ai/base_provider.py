from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    @abstractmethod
    async def complete(self, prompt: str) -> str:
        pass
