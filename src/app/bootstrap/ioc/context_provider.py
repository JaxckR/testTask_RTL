from typing import AsyncIterator

from dishka import Provider, Scope, from_context, provide
from httpx import AsyncClient

from app.bootstrap.config import PostgresConfig, Config, LLMConfig
from app.infrastructure.adapters import OpenRouterClient


class ContextProvider(Provider):
    scope = Scope.APP

    postgres = from_context(PostgresConfig)
    llm = from_context(LLMConfig)
    config = from_context(Config)

    @provide(scope=Scope.REQUEST)
    async def client(self) -> AsyncIterator[AsyncClient]:
        async with AsyncClient() as client:
            yield client

    @provide(scope=Scope.REQUEST)
    async def open_router_client(
        self, client: AsyncClient, config: Config
    ) -> OpenRouterClient:
        client.base_url = "https://openrouter.ai/api/v1"
        client.headers = {"Authorization": f"Bearer {config.llm.OPENROUTER_TOKEN}"}
        return OpenRouterClient(client)
