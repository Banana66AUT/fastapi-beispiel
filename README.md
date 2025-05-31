# YouTube Transcript API

Eine FastAPI-basierte API zum Abrufen von YouTube-Video-Transkripten mit API-Key-Authentifizierung und CORS-Unterstützung.

## Features

- 🎥 YouTube-Transcript-Extraktion
- 🔐 API-Key-Authentifizierung
- 🌐 CORS-Unterstützung
- 📚 Automatische API-Dokumentation
- ✅ Umfassende Fehlerbehandlung
- 🧪 Integrierte Tests

## Installation

1. **Dependencies installieren:**
```bash
pip install -r requirements.txt
```

2. **Umgebungsvariablen konfigurieren:**
```bash
# Kopiere die Beispiel-Konfiguration
cp env.example .env

# Bearbeite .env und setze deinen API-Key
API_KEY=dein-geheimer-api-key
```

## Server starten

### Option 1: Mit dem Startskript (empfohlen)
```bash
python start_server.py
```

### Option 2: Direkt mit uvicorn
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8082 --reload
```

Der Server läuft dann auf: `http://localhost:8082`

## API-Dokumentation

### Automatische Dokumentation
- **Swagger UI:** http://localhost:8082/docs
- **ReDoc:** http://localhost:8082/redoc

### Endpunkte

#### GET `/`
Basis-Endpunkt zum Testen der API.

**Response:**
```json
{
  "message": "FastAPI läuft!"
}
```

#### POST `/YTtranscript`
Ruft das Transcript eines YouTube-Videos ab.

**Headers:**
```
X-API-Key: dein-geheimer-api-key
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response (200):**
```json
{
  "transcript": "Das komplette Video-Transcript...",
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Error Responses:**
- `401`: Ungültiger API-Key
- `400`: Ungültige URL oder Transcript nicht verfügbar
- `500`: Interner Serverfehler

## Tests ausführen

```bash
# Stelle sicher, dass der Server läuft
python start_server.py

# In einem neuen Terminal:
python test_api.py
```

## Beispiel-Verwendung

### cURL
```bash
curl -X POST "http://localhost:8082/YTtranscript" \
  -H "X-API-Key: dein-geheimer-api-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=8gHt3fwub7U"}'
```

### Python
```python
import requests

url = "http://localhost:8082/YTtranscript"
headers = {
    "X-API-Key": "dein-geheimer-api-key",
    "Content-Type": "application/json"
}
data = {
    "url": "https://www.youtube.com/watch?v=8gHt3fwub7U"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### JavaScript/Fetch
```javascript
const response = await fetch('http://localhost:8082/YTtranscript', {
  method: 'POST',
  headers: {
    'X-API-Key': 'dein-geheimer-api-key',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=8gHt3fwub7U'
  })
});

const data = await response.json();
console.log(data);
```

## Konfiguration

### Umgebungsvariablen
- `API_KEY`: Der geheime API-Key für die Authentifizierung
- `HOST`: Server-Host (Standard: 0.0.0.0)
- `PORT`: Server-Port (Standard: 8082)

### CORS-Konfiguration
Die API ist standardmäßig für alle Origins konfiguriert. Für Produktionsumgebungen solltest du spezifische Origins in `app/main.py` angeben:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # Spezifische Origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Projektstruktur

```
fastapi-beispiel/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI-Anwendung
│   ├── auth.py              # API-Key-Authentifizierung
│   ├── config.py            # Konfiguration
│   ├── models.py            # Pydantic-Modelle
│   └── endpoints/
│       └── YTtranscript.py  # YouTube-Transcript-Logik
├── requirements.txt         # Python-Dependencies
├── start_server.py          # Server-Startskript
├── test_api.py             # API-Tests
├── env.example             # Beispiel-Umgebungskonfiguration
└── README.md               # Diese Datei
```

## Troubleshooting

### Häufige Probleme

1. **"Ungültiger API-Key"**
   - Stelle sicher, dass der `X-API-Key` Header gesetzt ist
   - Überprüfe, dass der API-Key korrekt konfiguriert ist

2. **"Ungültige YouTube-URL"**
   - Die URL muss den Parameter `v=` enthalten
   - Beispiel: `https://www.youtube.com/watch?v=VIDEO_ID`

3. **"Transcript nicht verfügbar"**
   - Nicht alle Videos haben Transkripte
   - Manche Videos haben nur automatisch generierte Transkripte
   - Private oder eingeschränkte Videos können nicht verarbeitet werden

4. **Server startet nicht**
   - Überprüfe, ob Port 8082 bereits verwendet wird
   - Installiere alle Dependencies: `pip install -r requirements.txt`

## Lizenz

Dieses Projekt ist für Bildungszwecke und Open-Source-Zwecke erstellt. Bitte beachte die YouTube-Nutzungsbedingungen bei der Verwendung. 