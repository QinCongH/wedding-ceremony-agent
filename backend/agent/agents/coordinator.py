from typing import Any

from agent.agents.base import BaseAgent


class CoordinatorAgent(BaseAgent):
    name = "coordinator"
    description = "协调各个子Agent，决定任务分配"

    async def run(self, input_text: str, **kwargs: Any) -> str:
        memory = kwargs.get("memory")
        # TODO: 接入LLM，根据意图路由到planner/executor
        return f"[Coordinator] 收到: {input_text}"
