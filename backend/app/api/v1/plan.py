from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def list_plans():
    return {"plans": []}


@router.post("")
async def create_plan():
    return {"message": "created"}
