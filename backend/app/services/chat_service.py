from sqlalchemy.ext.asyncio import AsyncSession

from agent.agents.coordinator import CoordinatorAgent
from agent.context import get_auth_token
from agent.memory.short_term import ShortTermMemory
from agent.state import AgentState
from shared.schemas.chat import ChatRequest, ChatResponse
from shared.schemas.user import UserInfo


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.agent = CoordinatorAgent()
        self.memory = ShortTermMemory()

    async def handle_chat(
        self, req: ChatRequest, user: UserInfo | None = None
    ) -> ChatResponse:
        # 需求 5：组装 AgentState，将鉴权 token 与用户信息随 run() 透传给 Agent
        if user is not None:
            state = AgentState(user=user, token=get_auth_token())
        else:
            state = AgentState.from_context()

        self.memory.add_user_message(req.message)
        result = await self.agent.run(req.message, state=state, memory=self.memory)
        self.memory.add_assistant_message(result)
        return ChatResponse(reply=result)
