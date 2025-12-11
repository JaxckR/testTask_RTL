from dishka import Provider, Scope, from_context

from app.bootstrap.config import PostgresConfig


class ContextProvider(Provider):
    scope = Scope.APP

    postgres = from_context(PostgresConfig)
