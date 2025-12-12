__all__ = ["map_tables", "mapper_registry", "video_table", "video_snapshot_table"]

import logging

from app.infrastructure.persistence.tables.base import mapper_registry
from app.infrastructure.persistence.tables.video import (
    map_video_table,
    map_video_snapshot_table,
    video_table,
    video_snapshot_table,
)

logger = logging.getLogger(__name__)


def map_tables() -> None:
    map_video_table()
    map_video_snapshot_table()

    logger.info("Tables mapped successfully")
