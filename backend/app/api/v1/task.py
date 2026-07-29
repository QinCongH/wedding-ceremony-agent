from fastapi import APIRouter

from shared.schemas.response import ApiResponse

router = APIRouter()


@router.get("")
async def list_tasks():
    return ApiResponse.success(data={"tasks": []})


@router.post("")
async def create_task():
    return ApiResponse.success(data={"message": "created"})
