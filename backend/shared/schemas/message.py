from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str
    session_id: str | None = None


class MessageOut(BaseModel):
    id: int
    user_id: int
    content: str
    session_id: str | None = None
    created_at: str
