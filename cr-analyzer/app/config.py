from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # CR API
    cr_api_base_url: str = "https://api.clashroyale.com/v1"
    cr_api_tokens: str = ""          # comma-separated list of API tokens

    # Redis
    redis_url: str = "redis://redis:6379"
    cache_ttl_seconds: int = 600     # 10 min default cache

    # Postgres
    database_url: str = "postgresql+asyncpg://cr:cr@postgres:5432/cr_analyzer"

    # App
    debug: bool = False
    log_level: str = "INFO"

    @property
    def token_list(self) -> List[str]:
        return [t.strip() for t in self.cr_api_tokens.split(",") if t.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
