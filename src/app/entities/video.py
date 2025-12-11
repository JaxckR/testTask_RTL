from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from app.entities.common import IDEntity

VideoId = NewType("VideoId", UUID)
VideoSnapshotId = NewType("VideoSnapshotId", str)


@dataclass
class Video(IDEntity[VideoId]):
    creator_id: str
    video_created_at: datetime
    views_count: int
    likes_count: int
    comments_count: int
    reports_count: int
    created_at: datetime
    updated_at: datetime | None


@dataclass
class VideoSnapshot(IDEntity[VideoSnapshotId]):
    video_id: VideoId
    views_count: int
    likes_count: int
    comments_count: int
    reports_count: int
    delta_views_count: int
    delta_likes_count: int
    delta_comments_count: int
    delta_reports_count: int
    created_at: datetime
    updated_at: datetime | None
