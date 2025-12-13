from dishka import Provider, Scope, provide

from app.application.ports import LLMGateway
from app.entities.repository import VideoRepository
from app.infrastructure.adapters import OpenRouterGateway
from app.infrastructure.persistence.adapters import VideoRepositoryImpl


class InfrastructureProvider(Provider):
    scope = Scope.REQUEST

    video_repository = provide(VideoRepositoryImpl, provides=VideoRepository)

    llm_gateway = provide(OpenRouterGateway, provides=LLMGateway)
