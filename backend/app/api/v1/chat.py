from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.deps import get_current_user
from shared.schemas.chat import ChatRequest, ChatResponse
from shared.schemas.response import ApiResponse
from shared.schemas.user import UserInfo
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("", response_model=ApiResponse[ChatResponse])
async def chat(
    req: ChatRequest,
    db: AsyncSession = Depends(get_db),
    user: UserInfo = Depends(get_current_user),
):
    service = ChatService(db=db)
    result = await service.handle_chat(req, user=user)
    return ApiResponse.success(data=result)
