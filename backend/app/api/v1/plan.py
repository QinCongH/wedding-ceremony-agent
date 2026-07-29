from fastapi import APIRouter

from shared.schemas.response import ApiResponse

router = APIRouter()


@router.get("")
async def list_plans():
    return ApiResponse.success(data={"plans": []})


@router.post("")
async def create_plan():
    return ApiResponse.success(data={"message": "created"})
