from typing import AsyncIterator

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.application.ports import TransactionManager
from app.bootstrap.config import PostgresConfig


class DatabaseProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def get_engine(self, config: PostgresConfig) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(
            config.url,
            pool_size=15,
            max_overflow=15,
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_sessionmaker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        async_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AnyOf[TransactionManager, AsyncSession]]:
        async with async_factory() as session:
            yield session
