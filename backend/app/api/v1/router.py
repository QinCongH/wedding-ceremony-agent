from fastapi import APIRouter

from app.api.v1.chat import router as chat_router
from app.api.v1.plan import router as plan_router
from app.api.v1.task import router as task_router

api_router = APIRouter()
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(plan_router, prefix="/plan", tags=["plan"])
api_router.include_router(task_router, prefix="/task", tags=["task"])
