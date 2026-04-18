from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1", alias="OPENAI_MODEL")
    openai_tool_mode: str = Field(default="function_fallback", alias="OPENAI_TOOL_MODE")
    openai_mcp_server_url: str | None = Field(default=None, alias="OPENAI_MCP_SERVER_URL")
    backend_cors_origins: str = Field(default="http://localhost:5173", alias="BACKEND_CORS_ORIGINS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
