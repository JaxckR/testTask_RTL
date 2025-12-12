import json
from typing import NewType, Final

from httpx import AsyncClient

from app.application.ports.llm_gateway import LLMGateway, AllowedActions
from app.entities.repository import VideoFilter

OpenRouterClient = NewType("LLMClient", AsyncClient)


class OpenRouterGateway(LLMGateway):
    PROMPT: Final[str] = """
You are a translator from natural-language input into a strictly defined JSON command.

IMPORTANT:
- The user's message will MOSTLY be in Russian.
- You MUST correctly understand Russian queries, dates, time expressions, numeric filters, and intent.
- You MUST NOT return "unknown" just because the text is in Russian.

You MUST read the field "message" and return a JSON object with the following EXACT structure:

{
  "action": "<one_of_allowed_actions>",
  "filters": {
    "id": null,
    "creator_id": null,
    "views": null,
    "views_gt": null,
    "views_lt": null,
    "created_at": null,
    "created_from": null,
    "created_to": null
  }
}

ALLOWED ACTIONS (use ONLY these values):
get_video
get_snapshot

IMPORTANT:
Different actions use DIFFERENT subsets of filters.
You MUST follow the action-specific filter rules that will be provided to you.
If a filter is not supported by the selected action — leave it null.
If a filter IS supported by the action and the user expresses that intent — fill it.

FILTER FIELD DEFINITIONS (STRICT):
- "id": string | null
  Specific object ID. ONLY when user explicitly specifies an identifier.

- "creator_id": string | null
  ID of the creator/author. ONLY when explicitly mentioned.

- "views": integer | null
  Exact number of views. ONLY when user requests an exact value.
  MUST NOT contain dates or text.

- "views_gt": integer | null
  Numeric threshold meaning “views greater than X”.
  MUST ALWAYS be a positive integer. NEVER dates.

- "views_lt": integer | null
  Numeric threshold meaning “views less than X”.
  MUST ALWAYS be a positive integer. NEVER dates.

- "created_at": ISO 8601 date | null
  Exact one-day date. ONLY for exact dates.

- "created_from": ISO 8601 date | null
  Start of a date range.

- "created_to": ISO 8601 date | null
  End of a date range.

DATE RULES:
- Dates MUST be ISO 8601 (YYYY-MM-DD or full timestamp).
- If user gives a date without a year (e.g. “25 ноября”), assume current year.
- You MUST correctly interpret Russian temporal expressions:
  “прошлая неделя”, “за последние 3 дня”, “вчера”, “с начала месяца”, etc.

GENERAL RULES:
1. The answer MUST be ONLY the JSON object. No markdown, no prose.
2. Use EXACTLY the fields shown above. Nothing more, nothing less.
3. If the action cannot be mapped to ANY allowed action — use:
   "action": "unknown".
4. NEVER output anything except the JSON object.

INPUT FORMAT:

{
  "command": "...this prompt...",
  "message": "<user text in Russian or another language>"
}

Your response MUST ALWAYS be ONLY the required JSON object.
"""

    def __init__(self, client: OpenRouterClient) -> None:
        self._client = client

    async def analyze(self, content: str) -> tuple[AllowedActions, VideoFilter]:
        response = await self._client.post(
            "/chat/completions",
            json={
                "model": "mistralai/devstral-2512:free",
                "messages": [
                    {
                        "role": "user",
                        "content": json.dumps(
                            {
                                "command": self.PROMPT,
                                "message": content,
                            }
                        ),
                    }
                ],
            },
        )
        data = json.loads(
            response.json().get("choices")[0].get("message").get("content")
        )
        return data.get("action"), VideoFilter(**data.get("filters"))
