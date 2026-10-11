from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"] = "user"

    content: str = Field(
        min_length=1,
        max_length=8000,
    )


class ChatRequest(BaseModel):
    session_id: str = Field(
        min_length=1,
        max_length=100,
    )

    message: str = Field(
        min_length=1,
        max_length=8000,
    )

    conversation: list[ChatMessage] = Field(
        default_factory=list,
        max_length=20,
    )


class ChatResponse(BaseModel):
    answer: str
    model: str
    provider: str
    session_id: str