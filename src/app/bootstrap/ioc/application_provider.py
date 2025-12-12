from dishka import Provider, Scope, provide_all

from app.application.handlers.nl2sql import NL2SQLHandler


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    handlers = provide_all(NL2SQLHandler)
