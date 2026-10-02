from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ModelResponse:
    content: str
    model: str
    provider: str


class ModelGateway(ABC):

    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, str]],
    ) -> ModelResponse:
        """Generate a model response."""
        raise NotImplementedError