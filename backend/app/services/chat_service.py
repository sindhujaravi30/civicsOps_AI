import logging
from time import perf_counter

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import Settings
from backend.app.db.models import ChatMessage, Conversation
from backend.app.models.chat import ChatRequest, ChatResponse
from backend.app.providers.base import ModelGateway


logger = logging.getLogger(__name__)


class ChatService:

    def __init__(
        self,
        model_gateway: ModelGateway,
        settings: Settings,
        db: AsyncSession,
    ):
        self.model_gateway = model_gateway
        self.settings = settings
        self.db = db

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        logger.info(
            "Resolving conversation session_id=%r",
            request.session_id,
        )
        conversation = await self._get_or_create_conversation(
            request.session_id
        )

        user_message = ChatMessage(
            conversation=conversation,
            role="user",
            content=request.message,
        )

        self.db.add(user_message)
        logger.info(
            "User message staged session_id=%r",
            request.session_id,
        )

        messages = [
            {
                "role": "system",
                "content": self.settings.system_prompt,
            }
        ]

        for message in request.conversation:
            messages.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": request.message,
            }
        )

        generation_started_at = perf_counter()
        logger.info(
            "Model generation started session_id=%r gateway=%s",
            request.session_id,
            type(self.model_gateway).__name__,
        )
        try:
            result = await self.model_gateway.generate(messages)
        except Exception as exc:
            logger.error(
                "Model generation failed session_id=%r gateway=%s "
                "error_type=%s",
                request.session_id,
                type(self.model_gateway).__name__,
                type(exc).__name__,
            )
            raise
        logger.info(
            "Model generation completed session_id=%r provider=%s "
            "model=%s duration_ms=%.2f",
            request.session_id,
            result.provider,
            result.model,
            (perf_counter() - generation_started_at) * 1000,
        )

        assistant_message = ChatMessage(
            conversation=conversation,
            role="assistant",
            content=result.content,
        )

        self.db.add(assistant_message)
        logger.info(
            "Persisting chat messages session_id=%r",
            request.session_id,
        )
        try:
            await self.db.commit()
        except SQLAlchemyError as exc:
            logger.error(
                "Chat message commit failed session_id=%r error_type=%s",
                request.session_id,
                type(exc).__name__,
            )
            await self.db.rollback()
            raise
        logger.info(
            "Chat messages persisted session_id=%r message_count=2",
            request.session_id,
        )

        return ChatResponse(
            answer=result.content,
            model=result.model,
            provider=result.provider,
            session_id=request.session_id,
        )

    async def _get_or_create_conversation(
        self,
        session_id: str,
    ) -> Conversation:

        result = await self.db.execute(
            select(Conversation).where(
                Conversation.session_id == session_id
            )
        )

        conversation = result.scalar_one_or_none()

        if conversation is None:
            logger.info(
                "Creating conversation session_id=%r",
                session_id,
            )
            conversation = Conversation(
                session_id=session_id,
            )

            self.db.add(conversation)

            await self.db.flush()
            logger.info(
                "Conversation created session_id=%r conversation_id=%s",
                session_id,
                conversation.id,
            )
        else:
            logger.info(
                "Conversation found session_id=%r conversation_id=%s",
                session_id,
                conversation.id,
            )

        return conversation