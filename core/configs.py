from typing import List, Optional, Any

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "sqlite:///cats.db"
    DBBaseModel: Optional[Any] = None

    class Config:

        case_sensitive = True


settings = Settings()
