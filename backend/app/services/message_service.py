from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from shared.schemas.message import MessageCreate, MessageOut


class MessageService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, data: MessageCreate) -> MessageOut:
        msg = Message(
            conversation_id=data.conversation_id,
            user_id=user_id,
            role=data.role,
            content=data.content,
        )
        self.db.add(msg)
        await self.db.flush()
        await self.db.refresh(msg)
        return MessageOut.model_validate(msg)

    async def get(self, message_id: int) -> Message | None:
        stmt = select(Message).where(Message.id == message_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, message_id: int, user_id: int) -> MessageOut:
        stmt = select(Message).where(Message.id == message_id)
        result = await self.db.execute(stmt)
        msg = result.scalar_one_or_none()
        if msg is None:
            raise MessageNotFound(message_id)
        if msg.user_id != user_id:
            raise NotOwner()
        await self.db.delete(msg)
        await self.db.flush()
        return MessageOut.model_validate(msg)


class MessageNotFound(Exception):
    def __init__(self, message_id: int) -> None:
        self.message_id = message_id
        super().__init__(f"message {message_id} not found")


class NotOwner(Exception):
    pass
