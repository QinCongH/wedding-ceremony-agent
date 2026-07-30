from fastapi import APIRouter

from app.api.v1.chat import router as chat_router
from app.api.v1.conversation import router as conversation_router
from app.api.v1.message import router as message_router
from app.api.v1.plan import router as plan_router
from app.api.v1.task import router as task_router
from app.api.v1.user import router as user_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(conversation_router, prefix="/conversation", tags=["conversation"])
api_router.include_router(message_router, prefix="/message", tags=["message"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(plan_router, prefix="/plan", tags=["plan"])
api_router.include_router(task_router, prefix="/task", tags=["task"])
