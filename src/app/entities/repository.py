from abc import abstractmethod
from typing import Protocol, Any

from app.entities.video import Video


class VideoRepository(Protocol):
    @abstractmethod
    async def get_count(self) -> int: ...

    @abstractmethod
    async def raw(self, stmt: str) -> Any: ...

    @abstractmethod
    def add(self, instance: Video) -> None: ...
