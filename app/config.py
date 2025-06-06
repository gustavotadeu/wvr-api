import os
from functools import lru_cache

class Settings:
    api_v1_prefix: str = "/api/v1"
    admin_token: str = os.getenv("ADMIN_TOKEN", "changeme")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

@lru_cache
def get_settings():
    return Settings()
