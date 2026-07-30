from datetime import datetime

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    title: str | None = None


class ConversationOut(BaseModel):
    id: int
    thread_id: str
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedConversations(BaseModel):
    items: list[ConversationOut]
    total: int
    page: int
    page_size: int


class ConversationDetailOut(ConversationOut):
    messages: list["MessageOut"] = []

    model_config = {"from_attributes": True}


from shared.schemas.message import MessageOut  # noqa: E402

ConversationDetailOut.model_rebuild()
