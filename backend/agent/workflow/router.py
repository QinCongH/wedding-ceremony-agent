from agent.agents.base import BaseAgent


class AgentRouter:
    """根据意图路由到对应Agent"""

    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}

    def register(self, name: str, agent: BaseAgent):
        self._agents[name] = agent

    def route(self, intent: str) -> BaseAgent | None:
        # TODO: 接入LLM做意图分类
        return self._agents.get("coordinator")
