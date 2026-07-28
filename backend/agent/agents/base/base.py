import os
from typing import Any

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage

from agent.agents.base_agent import BaseAgent
from agent.context import get_auth_token, get_auth_user
from agent.state import AgentState

SYSTEM_PROMPT = """\
可咨询任何婚礼相关问题
"""


class WeddingBaseAgent(BaseAgent):
    name = "Base"
    description = "婚礼策划工程师"

    def __init__(self) -> None:
        model = init_chat_model(
            model="xopkimik26",
            model_provider="openai",
            base_url=os.getenv("XUNFEI_BASE_URL"),
            api_key=os.getenv("XUNFEI_API_KEY"),
        )
        self._agent = create_agent(model=model, system_prompt=SYSTEM_PROMPT)

    async def run(self, input_text: str, state: AgentState | None = None, **kwargs: Any) -> str:
        # 需求 5：从 context 取 token，从 AgentState 取用户信息
        token = state.token if state else get_auth_token()
        user = state.user if state else get_auth_user()

        # 可在此处将 user / token 注入 Prompt 或工具鉴权
        # （对接 .agent/鉴权/需求.md 的动态提示词与工具鉴权）
        sys_prompt = SYSTEM_PROMPT
        if user:
            sys_prompt += f"\n当前用户：{user.nickname}({user.username})"

        res = await self._agent.ainvoke({"messages": [HumanMessage(input_text)]})
        return res["messages"][-1].content


if __name__ == "__main__":
    import asyncio

    from dotenv import load_dotenv

    load_dotenv()

    agent = WeddingBaseAgent()
    result = asyncio.run(agent.run("中秋节日结婚"))
    print(result)
