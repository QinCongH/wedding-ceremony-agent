from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_mysql_db
from app.deps import get_current_user
from app.services.message_service import MessageService, MessageNotFound, NotOwner
from shared.schemas.message import MessageCreate, MessageOut
from shared.schemas.response import ApiResponse
from shared.schemas.user import UserInfo

router = APIRouter()


@router.post("", response_model=ApiResponse[MessageOut], status_code=status.HTTP_201_CREATED)
async def send_message(
    req: MessageCreate,
    user: UserInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_db),
):
    svc = MessageService(db)
    result = await svc.create(user_id=user.id, data=req)
    await db.commit()
    return ApiResponse.success(data=result)


@router.delete("/{message_id}", response_model=ApiResponse[MessageOut])
async def delete_message(
    message_id: int,
    user: UserInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_mysql_db),
):
    svc = MessageService(db)
    try:
        result = await svc.delete(message_id, user_id=user.id)
        await db.commit()
        return ApiResponse.success(data=result)
    except MessageNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "message_not_found")
    except NotOwner:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "cannot_delete_others_message")
