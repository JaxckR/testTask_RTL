from typing import Any

from sqlalchemy import select, text
from sqlalchemy.sql.functions import func

from app.entities.repository import VideoRepository
from app.entities.video import Video
from app.infrastructure.persistence.adapters.mixins import SQLAMixin


class VideoRepositoryImpl(SQLAMixin, VideoRepository):
    async def get_count(self) -> int:
        query = await self._session.execute(select(func.count(Video.id)))
        return query.scalar()

    async def raw(self, stmt: str) -> Any:
        query = await self._session.execute(text(stmt))
        return query.scalar_one_or_none()

    def add(self, instance: Video) -> None:
        self._session.add(instance)
