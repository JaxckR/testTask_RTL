__all__ = ["providers"]

from dishka import Provider

from app.bootstrap.ioc.application_provider import ApplicationProvider
from app.bootstrap.ioc.context_provider import ContextProvider
from app.bootstrap.ioc.database_provider import DatabaseProvider
from app.bootstrap.ioc.infrastructure_provider import InfrastructureProvider


def providers() -> list[Provider]:
    return [
        ContextProvider(),
        DatabaseProvider(),
        ApplicationProvider(),
        InfrastructureProvider(),
    ]
