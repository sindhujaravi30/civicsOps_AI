from backend.app.core.config import Settings
from backend.app.models.chat import ChatRequest, ChatResponse
from backend.app.providers.base import ModelGateway


class ChatService:

    def __init__(
        self,
        model_gateway: ModelGateway,
        settings: Settings,
    ):
        self.model_gateway = model_gateway
        self.settings = settings

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

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

        result = await self.model_gateway.generate(
            messages
        )

        return ChatResponse(
            answer=result.content,
            model=result.model,
            provider=result.provider,
        )