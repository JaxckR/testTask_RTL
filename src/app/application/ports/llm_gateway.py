from abc import abstractmethod
from typing import Protocol


class LLMGateway(Protocol):
    @abstractmethod
    async def analyze(self, content: str) -> str | None: ...
