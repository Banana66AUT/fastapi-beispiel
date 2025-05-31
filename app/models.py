from pydantic import BaseModel, HttpUrl
from typing import Optional

class YouTubeRequest(BaseModel):
    url: HttpUrl
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=8gHt3fwub7U"
            }
        }

class TranscriptResponse(BaseModel):
    transcript: str
    video_url: str
    
class ErrorResponse(BaseModel):
    detail: str 