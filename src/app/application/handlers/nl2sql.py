from typing import Any

from app.application.ports.llm_gateway import LLMGateway, AllowedActions
from app.entities.repository import VideoRepository


class NL2SQLHandler:
    def __init__(
        self,
        video_repository: VideoRepository,
        llm_gateway: LLMGateway,
    ) -> None:
        self._video_repository = video_repository
        self._llm_gateway = llm_gateway

    async def handle(self, data: str) -> Any:
        action, filters = await self._llm_gateway.analyze(content=data)
        print(action, filters)

        if action == AllowedActions.GET_VIDEO:
            return await self._video_repository.get_count(filters=filters)
