from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: int
    content: str
    role: str = "user"


class MessageOut(BaseModel):
    id: int
    conversation_id: int
    user_id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
