from pydantic import BaseModel, HttpUrl
from typing import Optional

class YouTubeRequest(BaseModel):
    url: HttpUrl
    languages: Optional[list[str]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=8gHt3fwub7U",
                "languages": ["de", "en"]
            }
        }

class TranscriptResponse(BaseModel):
    transcript: str
    video_url: str
    language: str
    video_id: str
    
class ErrorResponse(BaseModel):
    detail: str 