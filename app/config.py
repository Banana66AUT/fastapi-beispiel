import os
from typing import Optional

class Settings:
    API_KEY: str = os.getenv("API_KEY", "dein-geheimer-api-key")
    API_KEY_NAME: str = "X-API-Key"
    
settings = Settings() 