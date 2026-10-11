import logging
from time import perf_counter

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import Settings, get_settings
from backend.app.db.session import get_db_session
from backend.app.models.chat import ChatRequest, ChatResponse
from backend.app.providers.groq import GroqProvider
from backend.app.services.chat_service import ChatService


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/v1",
    tags=["chat"],
)


def get_chat_service(
    settings: Settings = Depends(get_settings),
    db: AsyncSession = Depends(get_db_session),
) -> ChatService:

    try:
        provider = GroqProvider(settings)

    except ValueError as exc:
        logger.error("Chat provider configuration failed: %s", exc)
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    return ChatService(
        model_gateway=provider,
        settings=settings,
        db=db,
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    started_at = perf_counter()
    logger.info(
        "Chat request received session_id=%r history_messages=%d",
        request.session_id,
        len(request.conversation),
    )

    try:
        response = await service.chat(request)
        logger.info(
            "Chat request completed session_id=%r provider=%s model=%s "
            "duration_ms=%.2f",
            request.session_id,
            response.provider,
            response.model,
            (perf_counter() - started_at) * 1000,
        )
        return response

    except SQLAlchemyError as exc:
        logger.error(
            "Chat request failed during database persistence "
            "session_id=%r error_type=%s duration_ms=%.2f",
            request.session_id,
            type(exc).__name__,
            (perf_counter() - started_at) * 1000,
        )

        raise HTTPException(
            status_code=500,
            detail="The conversation could not be saved.",
        ) from exc

    except Exception as exc:
        logger.error(
            "Chat request failed session_id=%r error_type=%s "
            "duration_ms=%.2f",
            request.session_id,
            type(exc).__name__,
            (perf_counter() - started_at) * 1000,
        )

        raise HTTPException(
            status_code=502,
            detail="The AI provider could not process the request.",
        ) from exc