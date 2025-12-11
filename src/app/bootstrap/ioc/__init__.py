__all__ = ["providers"]

from dishka import Provider

from app.bootstrap.ioc.context_provider import ContextProvider
from app.bootstrap.ioc.database_provider import DatabaseProvider


def providers() -> list[Provider]:
    return [
        ContextProvider(),
        DatabaseProvider(),
    ]
