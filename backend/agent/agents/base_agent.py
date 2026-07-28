from abc import ABC, abstractmethod
from typing import Any

from agent.state import AgentState


class BaseAgent(ABC):
    name: str = ""
    description: str = ""

    @abstractmethod
    async def run(
        self, input_text: str, state: AgentState | None = None, **kwargs: Any
    ) -> str:
        """执行 Agent 逻辑。

        :param state: Agent 运行时状态（用户信息 / 鉴权 token / 扩展字段），
                      由 Service 层通过 ``AgentState.from_context()`` 注入。
        """
        raise NotImplementedError
