import asyncio
import json
import os
import sys
from argparse import ArgumentParser

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.bootstrap.config import config
from app.entities.video import VideoSnapshot, Video
from app.infrastructure.persistence.adapters.video import VideoRepositoryImpl
from app.infrastructure.persistence.tables import map_tables

map_tables()

engine = create_async_engine(
    config.postgres.url,
    pool_size=15,
    max_overflow=15,
)

sessionmaker = async_sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Loader:
    def __init__(
        self,
        filename: str,
        *_,
        video_repository: VideoRepositoryImpl,
    ) -> None:
        if filename.startswith("/"):
            filename = filename[1:]

        self.path = f"{filename}"
        self.repository = video_repository

        if not os.path.exists(self.path):
            raise Exception("Path does not exist")

    def read(self) -> dict:
        with open(f"{self.path}", "r") as file:
            file = file.read()
            return json.loads(file).get("videos")

    async def save(self) -> None:
        data = self.read()
        for video_dict in data:
            snapshots = []
            for snapshot in video_dict.get("snapshots"):
                snapshots.append(VideoSnapshot(**snapshot))

            if video_dict.get("snapshots"):
                del video_dict["snapshots"]

            self.repository.add(Video(**video_dict, snapshots=snapshots))
            await self.repository._session.commit()


async def main(filename: str) -> None:
    async with sessionmaker() as session:
        loader = Loader(
            filename,
            video_repository=VideoRepositoryImpl(
                session=session,
            ),
        )
        await loader.save()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()

    asyncio.run(main(args.filename))
