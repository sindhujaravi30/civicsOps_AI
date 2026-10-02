from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CivicOps AI"
    app_version: str = "1.0.0"
    environment: str = "development"

    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"

    # Keep this configurable because Groq's available model catalog can change.
    groq_model: str = "openai/gpt-oss-120b"

    llm_timeout_seconds: float = 30.0

    system_prompt: str = (
        "You are CivicOps AI, a helpful government-service assistant. "
        "Answer clearly and concisely. "
        "Do not invent government policies, fees, deadlines, or personal data. "
        "If information is unavailable, say so explicitly."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()