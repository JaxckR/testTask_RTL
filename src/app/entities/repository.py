from abc import abstractmethod
from datetime import datetime
from typing import Protocol

from pydantic.dataclasses import dataclass

from app.entities.video import Video, VideoId


@dataclass(kw_only=True)
class VideoFilter:
    id: VideoId | None = None
    creator_id: str | None = None
    views: int | None = None
    views_lt: int | None = None
    views_gt: int | None = None
    created_at: datetime | None = None
    created_from: datetime | None = None
    created_to: datetime | None = None


class VideoRepository(Protocol):
    @abstractmethod
    async def get_count(self, filters: VideoFilter | None = None) -> int: ...

    @abstractmethod
    def add(self, instance: Video) -> None: ...
