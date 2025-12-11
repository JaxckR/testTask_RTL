__all__ = ["map_tables", "mapper_registry", "video_table", "video_snapshot_table"]

from app.infrastructure.persistence.tables.base import mapper_registry
from app.infrastructure.persistence.tables.video import (
    map_video_table,
    map_video_snapshot_table,
    video_table,
    video_snapshot_table,
)


def map_tables() -> None:
    map_video_table()
    map_video_snapshot_table()
