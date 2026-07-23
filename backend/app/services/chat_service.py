from sqlalchemy.ext.asyncio import AsyncSession

from agent.agents.coordinator import CoordinatorAgent
from agent.memory.short_term import ShortTermMemory
from shared.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.agent = CoordinatorAgent()
        self.memory = ShortTermMemory()

    async def handle_chat(self, req: ChatRequest) -> ChatResponse:
        self.memory.add_user_message(req.message)
        result = await self.agent.run(req.message, memory=self.memory)
        self.memory.add_assistant_message(result)
        return ChatResponse(reply=result)
