from typing import Any

from agent.agents.base import BaseAgent


class ExecutorAgent(BaseAgent):
    name = "executor"
    description = "执行具体任务，调用工具完成操作"

    async def run(self, input_text: str, **kwargs: Any) -> str:
        # TODO: 接入LLM + tools，执行具体操作
        return f"[Executor] 执行中: {input_text}"
