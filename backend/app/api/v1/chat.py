from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db=db)
    result = await service.handle_chat(req)
    return result
