from openai import AsyncOpenAI

from backend.app.core.config import Settings
from backend.app.providers.base import ModelGateway, ModelResponse


class GroqProvider(ModelGateway):

    def __init__(self, settings: Settings):
        if not settings.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.model = settings.groq_model

        self.client = AsyncOpenAI(
            api_key=settings.groq_api_key,
            base_url=settings.groq_base_url,
            timeout=settings.llm_timeout_seconds,
        )

    async def generate(
        self,
        messages: list[dict[str, str]],
    ) -> ModelResponse:

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "The model returned an empty response."
            )

        return ModelResponse(
            content=content,
            model=self.model,
            provider="groq",
        )