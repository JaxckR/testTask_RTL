import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.entities.video import Video, VideoSnapshot
from app.infrastructure.persistence.tables.base import mapper_registry

video_table = sa.Table(
    "videos",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("creator_id", sa.String),
    sa.Column("video_created_at", sa.DateTime),
    sa.Column("views_count", sa.Integer),
    sa.Column("likes_count", sa.Integer),
    sa.Column("comments_count", sa.Integer),
    sa.Column("reports_count", sa.Integer),
    sa.Column("created_at", sa.DateTime),
    sa.Column("updated_at", sa.DateTime),
)

video_snapshot_table = sa.Table(
    "video_snapshots",
    mapper_registry.metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("video_id", sa.UUID(as_uuid=True), sa.ForeignKey("videos.id")),
    sa.Column("views_count", sa.Integer),
    sa.Column("likes_count", sa.Integer),
    sa.Column("comments_count", sa.Integer),
    sa.Column("reports_count", sa.Integer),
    sa.Column("delta_views_count", sa.Integer),
    sa.Column("delta_likes_count", sa.Integer),
    sa.Column("delta_comments_count", sa.Integer),
    sa.Column("delta_reports_count", sa.Integer),
    sa.Column("created_at", sa.DateTime),
    sa.Column("updated_at", sa.DateTime),
)


def map_video_table() -> None:
    _ = mapper_registry.map_imperatively(
        Video,
        video_table,
        properties={
            "id": video_table.c.id,
            "creator_id": video_table.c.creator_id,
            "video_created_at": video_table.c.video_created_at,
            "views_count": video_table.c.views_count,
            "likes_count": video_table.c.likes_count,
            "comments_count": video_table.c.comments_count,
            "reports_count": video_table.c.reports_count,
            "created_at": video_table.c.created_at,
            "updated_at": video_table.c.updated_at,
            "snapshots": relationship(
                VideoSnapshot,
                lazy="selectin",
            ),
        },
        column_prefix="_",
    )


def map_video_snapshot_table() -> None:
    _ = mapper_registry.map_imperatively(
        VideoSnapshot,
        video_snapshot_table,
        properties={
            "id": video_snapshot_table.c.id,
            "video_id": video_snapshot_table.c.video_id,
            "views_count": video_snapshot_table.c.views_count,
            "likes_count": video_snapshot_table.c.likes_count,
            "comments_count": video_snapshot_table.c.comments_count,
            "reports_count": video_snapshot_table.c.reports_count,
            "delta_views_count": video_snapshot_table.c.delta_views_count,
            "delta_likes_count": video_snapshot_table.c.delta_likes_count,
            "delta_comments_count": video_snapshot_table.c.delta_comments_count,
            "delta_reports_count": video_snapshot_table.c.delta_reports_count,
            "created_at": video_snapshot_table.c.created_at,
            "updated_at": video_snapshot_table.c.updated_at,
        },
        column_prefix="_",
    )
