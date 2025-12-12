from dishka import Provider, Scope, provide

from app.application.ports.llm_gateway import LLMGateway
from app.entities.repository import VideoRepository
from app.infrastructure.adapters.llm_gateway import OpenRouterGateway
from app.infrastructure.persistence.adapters.video import VideoRepositoryImpl


class InfrastructureProvider(Provider):
    scope = Scope.REQUEST

    video_repository = provide(VideoRepositoryImpl, provides=VideoRepository)

    llm_gateway = provide(OpenRouterGateway, provides=LLMGateway)
