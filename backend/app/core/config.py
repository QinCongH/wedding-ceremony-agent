from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Wedding Ceremony Agent"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "sqlite+aiosqlite:///./data.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4o"
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = ""

    AGENT_MAX_ITERATIONS: int = 10
    AGENT_TIMEOUT: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
