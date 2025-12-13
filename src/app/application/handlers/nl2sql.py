from typing import Any

from app.application.ports import LLMGateway
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
        sql = await self._llm_gateway.analyze(content=data)

        if sql is None:
            return "Произошли проблемы на стороне llm провайдера :("

        if sql:
            return await self._video_repository.raw(sql)
