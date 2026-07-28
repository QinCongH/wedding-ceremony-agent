"""消息模块：发送消息 / 删除消息。对应技术文档 §6.2。"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_current_user
from app.services.message_service import MessageService, NotFound, NotOwner
from shared.schemas.message import MessageCreate, MessageOut
from shared.schemas.user import UserInfo

router = APIRouter()


@router.post("", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def send_message(
    req: MessageCreate,
    user: UserInfo = Depends(get_current_user),
):
    return MessageService().create(
        content=req.content,
        user_id=user.id,
        session_id=req.session_id,
    )


@router.delete("/{message_id}", response_model=MessageOut)
async def delete_message(
    message_id: int,
    user: UserInfo = Depends(get_current_user),
):
    try:
        return MessageService().delete(message_id, user_id=user.id)
    except NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "message_not_found")
    except NotOwner:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "cannot_delete_others_message")
