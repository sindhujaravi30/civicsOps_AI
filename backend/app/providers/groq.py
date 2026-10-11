import logging
from time import perf_counter

from openai import AsyncOpenAI

from backend.app.core.config import Settings
from backend.app.providers.base import ModelGateway, ModelResponse


logger = logging.getLogger(__name__)


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
        started_at = perf_counter()
        logger.info(
            "Groq request started model=%s message_count=%d",
            self.model,
            len(messages),
        )
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
            )
        except Exception as exc:
            logger.error(
                "Groq request failed model=%s error_type=%s",
                self.model,
                type(exc).__name__,
            )
            raise

        content = response.choices[0].message.content

        if not content:
            logger.error("Groq returned an empty response model=%s", self.model)
            raise RuntimeError(
                "The model returned an empty response."
            )

        logger.info(
            "Groq request completed model=%s duration_ms=%.2f",
            self.model,
            (perf_counter() - started_at) * 1000,
        )
        return ModelResponse(
            content=content,
            model=self.model,
            provider="groq",
        )