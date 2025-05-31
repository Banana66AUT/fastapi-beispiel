from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .endpoints.YTtranscript import LoadTranscript
from .auth import get_api_key
from .models import YouTubeRequest, TranscriptResponse, ErrorResponse

app = FastAPI(
    title="YouTube Transcript API",
    description="API zum Abrufen von YouTube-Video-Transkripten",
    version="1.0.0"
)

# CORS-Middleware hinzufügen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion spezifische Origins angeben
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FastAPI läuft!"}

@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon"}

@app.post(
    "/YTtranscript",
    response_model=TranscriptResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Ungültiger API-Key"},
        400: {"model": ErrorResponse, "description": "Ungültige YouTube-URL oder Transcript nicht verfügbar"},
        500: {"model": ErrorResponse, "description": "Interner Serverfehler"}
    },
    summary="YouTube-Transcript abrufen",
    description="Ruft das Transcript eines YouTube-Videos ab. Benötigt einen gültigen API-Key."
)
async def get_youtube_transcript(
    request: YouTubeRequest,
    api_key: str = Depends(get_api_key)
):
    try:
        transcript_loader = LoadTranscript(str(request.url))
        result = transcript_loader.run()
        
        return TranscriptResponse(
            transcript=result["transcript"],
            video_url=str(request.url)
        )
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ungültige YouTube-URL. Stellen Sie sicher, dass die URL einen 'v=' Parameter enthält."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fehler beim Abrufen des Transcripts: {str(e)}"
        )
