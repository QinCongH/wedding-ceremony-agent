from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from app.models.message import Message
from shared.schemas.conversation import ConversationCreate, ConversationOut, ConversationDetailOut, PaginatedConversations
from shared.schemas.message import MessageOut


class ConversationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, data: ConversationCreate) -> ConversationOut:
        conv = Conversation(
            user_id=user_id,
            title=data.title or "新会话",
        )
        self.db.add(conv)
        await self.db.flush()
        await self.db.refresh(conv)
        return ConversationOut.model_validate(conv)

    async def list_by_user(self, user_id: int, page: int = 1, page_size: int = 20) -> PaginatedConversations:
        # 总数
        count_stmt = select(func.count()).select_from(Conversation).where(Conversation.user_id == user_id)
        total = (await self.db.execute(count_stmt)).scalar() or 0

        # 分页数据
        offset = (page - 1) * page_size
        stmt = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        result = await self.db.execute(stmt)
        items = [ConversationOut.model_validate(c) for c in result.scalars().all()]
        return PaginatedConversations(items=items, total=total, page=page, page_size=page_size)

    async def get_messages(self, conversation_id: int, user_id: int) -> ConversationDetailOut:
        conv = await self._get_owned(conversation_id, user_id)
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        result = await self.db.execute(stmt)
        messages = [MessageOut.model_validate(m) for m in result.scalars().all()]
        conv_out = ConversationOut.model_validate(conv)
        return ConversationDetailOut(**conv_out.model_dump(), messages=messages)

    async def delete(self, conversation_id: int, user_id: int) -> None:
        conv = await self._get_owned(conversation_id, user_id)
        await self.db.delete(conv)
        await self.db.flush()

    async def _get_owned(self, conversation_id: int, user_id: int) -> Conversation:
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        result = await self.db.execute(stmt)
        conv = result.scalar_one_or_none()
        if conv is None:
            raise ConversationNotFound(conversation_id)
        return conv


class ConversationNotFound(Exception):
    def __init__(self, conversation_id: int) -> None:
        self.conversation_id = conversation_id
        super().__init__(f"conversation {conversation_id} not found")
