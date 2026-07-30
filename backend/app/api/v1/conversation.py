from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_mysql_db
from app.deps import get_current_user
from app.services.conversation_service import ConversationService, ConversationNotFound
from shared.schemas.conversation import ConversationCreate, ConversationOut, ConversationDetailOut, PaginatedConversations
from shared.schemas.response import ApiResponse
from shared.schemas.user import UserInfo

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("", response_model=ApiResponse[ConversationOut], status_code=status.HTTP_201_CREATED)
async def create_conversation(
    req: ConversationCreate,
    user: UserInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_db),
):
    svc = ConversationService(db)
    result = await svc.create(user_id=user.id, data=req)
    await db.commit()
    return ApiResponse.success(data=result)


@router.get("", response_model=ApiResponse[PaginatedConversations])
async def list_conversations(
    page: int = 1,
    page_size: int = 20,
    user: UserInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_db),
):
    svc = ConversationService(db)
    result = await svc.list_by_user(user_id=user.id, page=page, page_size=page_size)
    return ApiResponse.success(data=result)


@router.delete("/{conversation_id}", response_model=ApiResponse[None])
async def delete_conversation(
    conversation_id: int,
    user: UserInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_db),
):
    svc = ConversationService(db)
    try:
        await svc.delete(conversation_id=conversation_id, user_id=user.id)
        await db.commit()
        return ApiResponse.success()
    except ConversationNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "conversation_not_found")


@router.get(
    "messages/{conversation_id}",
    response_model=ApiResponse[ConversationDetailOut],
)
async def get_conversation_messages(
    conversation_id: int,
    user: UserInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_db),
):
    svc = ConversationService(db)
    try:
        result = await svc.get_messages(conversation_id=conversation_id, user_id=user.id)
        return ApiResponse.success(data=result)
    except ConversationNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "conversation_not_found")
