import uvicorn
import os

if __name__ == "__main__":
    # Setze den API-Key als Umgebungsvariable falls nicht gesetzt
if not os.getenv("API_KEY"):
    os.environ["API_KEY"] = "dein-geheimer-api-key"
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8082,
        reload=True,
        log_level="info"
    ) 