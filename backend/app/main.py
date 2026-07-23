"""Wedding Ceremony Agent - Backend Application"""

from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="婚礼仪式智能体后端服务",
    )

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.on_event("startup")
    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return app


app = create_app()
