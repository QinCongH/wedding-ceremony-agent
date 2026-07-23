from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    name: str = ""
    description: str = ""

    @abstractmethod
    async def run(self, input_text: str, **kwargs: Any) -> str:
        raise NotImplementedError
