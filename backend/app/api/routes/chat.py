from fastapi import APIRouter, Depends, HTTPException

from backend.app.core.config import Settings, get_settings
from backend.app.models.chat import ChatRequest, ChatResponse
from backend.app.providers.groq import GroqProvider
from backend.app.services.chat_services import ChatService


router = APIRouter(
    prefix="/api/v1",
    tags=["chat"],
)


def get_chat_service(
    settings: Settings = Depends(get_settings),
) -> ChatService:

    try:
        provider = GroqProvider(settings)

    except ValueError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    return ChatService(
        model_gateway=provider,
        settings=settings,
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    try:
        return await service.chat(request)

    except Exception as exc:
        print(f"LLM provider error: {type(exc).__name__}: {exc}")

        raise HTTPException(
            status_code=502,
            detail=f"AI provider error: {type(exc).__name__}: {exc}",
        ) from exc