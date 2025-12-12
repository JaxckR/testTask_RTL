from abc import abstractmethod
from enum import StrEnum
from typing import Protocol

from app.entities.repository import VideoFilter


class AllowedActions(StrEnum):
    GET_VIDEO = "get_video"
    GET_SNAPSHOT = "get_snapshot"


class LLMGateway(Protocol):
    @abstractmethod
    async def analyze(self, content: str) -> tuple[AllowedActions, VideoFilter]: ...
