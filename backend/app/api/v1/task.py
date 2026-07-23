from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def list_tasks():
    return {"tasks": []}


@router.post("")
async def create_task():
    return {"message": "created"}
