from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv  
import os  
load_dotenv()  

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",  # 忽略 .env 中未在模型中声明的字段（如 zhipu_*/xunfei_*，供 os.getenv 使用）
        env_file=".env",
        env_file_encoding="utf-8",
    )

    PROJECT_NAME: str = "Wedding Ceremony Agent"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "sqlite+aiosqlite:///./data.db"
    MYSQL_DATABASE_URL: str = os.getenv("MYSQL_DATABASE_URL")
    REDIS_URL: str = "redis://localhost:6379/0"

    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4o"
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = ""

    AGENT_MAX_ITERATIONS: int = 10
    AGENT_TIMEOUT: int = 60

    # JWT 鉴权配置
    JWT_SECRET: str = "change-me-in-prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 天


settings = Settings()
