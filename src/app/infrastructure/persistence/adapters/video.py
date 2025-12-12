from sqlalchemy import select, Select, and_
from sqlalchemy.sql.functions import func

from app.entities.repository import VideoRepository, VideoFilter
from app.entities.video import Video
from app.infrastructure.persistence.adapters.mixins import SQLAMixin


class VideoRepositoryImpl(SQLAMixin, VideoRepository):
    @staticmethod
    def use_filters(query: Select, filters: VideoFilter) -> Select:
        if filters.id:
            query = query.where(and_(Video.id == filters.id))
        if filters.creator_id:
            query = query.where(and_(Video.creator_id == filters.creator_id))
        if filters.views:
            query = query.where(and_(Video.views_count == filters.views))
        if filters.views_lt:
            query = query.where(and_(Video.views_count < filters.views_lt))
        if filters.views_gt:
            query = query.where(and_(Video.views_count > filters.views_gt))
        if filters.created_at:
            query = query.where(and_(Video.created_at == filters.created_at))
        if filters.created_from:
            query = query.where(and_(Video.created_at >= filters.created_from))
        if filters.created_to:
            query = query.where(and_(Video.created_at <= filters.created_to))

        return query

    async def get_count(self, filters: VideoFilter | None = None) -> int:
        query = await self._session.execute(
            self.use_filters(select(func.count(Video.id)), filters)
        )
        return query.scalar()

    def add(self, instance: Video) -> None:
        self._session.add(instance)
