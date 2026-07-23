from typing import Any

from agent.agents.base import BaseAgent


class PlannerAgent(BaseAgent):
    name = "planner"
    description = "负责婚礼方案规划和生成"

    async def run(self, input_text: str, **kwargs: Any) -> str:
        # TODO: 接入LLM，生成婚礼方案
        return f"[Planner] 规划中: {input_text}"
