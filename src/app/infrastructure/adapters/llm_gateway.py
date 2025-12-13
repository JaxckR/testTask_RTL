import json
from typing import NewType

from httpx import AsyncClient

from app.application.exceptions import TokensExpiredError
from app.application.ports import LLMGateway
from app.bootstrap.config import LLMConfig

OpenRouterClient = NewType("LLMClient", AsyncClient)


class OpenRouterGateway(LLMGateway):
    def __init__(self, client: OpenRouterClient, config: LLMConfig) -> None:
        self._client = client
        self._config = config

    async def analyze(self, content: str) -> str | None:
        response = await self._client.post(
            "/chat/completions",
            json={
                "model": "mistralai/devstral-2512:free",
                "messages": [
                    {
                        "role": "user",
                        "content": json.dumps(
                            {
                                "command": self._config.prompt,
                                "message": content,
                            }
                        ),
                    }
                ],
            },
        )
        json_response = response.json()
        if "error" in json_response:
            if json_response["error"].get("code") == 429:
                raise TokensExpiredError
            return None
        return json.loads(
            response.json().get("choices")[0].get("message").get("content")
        ).get("sql")
