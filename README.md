# YouTube Transcript API

Eine FastAPI-basierte API zum Abrufen von YouTube-Video-Transkripten mit API-Key-Authentifizierung und CORS-Unterstützung.

## Features

- 🎥 YouTube-Transcript-Extraktion
- 🔐 API-Key-Authentifizierung
- 🌐 CORS-Unterstützung
- 📚 Automatische API-Dokumentation
- ✅ Umfassende Fehlerbehandlung
- 🧪 Integrierte Tests (synchron & asynchron)
- 🚀 Asynchrone Test-Suite mit Multithreading
- ⚡ Performance-Benchmarking
- 📊 Detaillierte Ausführungsmetriken

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
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "languages": ["de", "en"]
}
```

**Response (200):**
```json
{
  "transcript": "Das komplette Video-Transcript...",
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "language": "de",
  "video_id": "VIDEO_ID"
}
```

**Error Responses:**
- `401`: Ungültiger API-Key
- `400`: Ungültige URL oder Transcript nicht verfügbar
- `500`: Interner Serverfehler

## Tests ausführen

### Synchrone Tests (Standard)
```bash
# Stelle sicher, dass der Server läuft
python start_server.py

# In einem neuen Terminal:
python test_api.py
```

### Asynchrone Tests mit Multithreading
```bash
# Stelle sicher, dass der Server läuft
python start_server.py

# In einem neuen Terminal - Asynchrone Tests:
python test_api_async.py
```

Die asynchrone Version bietet folgende Vorteile:
- **🚀 Parallele Ausführung**: Alle Tests laufen gleichzeitig
- **⚡ Performance-Vergleich**: Zeigt Speedup gegenüber sequenzieller Ausführung
- **📊 Detaillierte Metriken**: Ausführungszeiten für jeden Test
- **🔄 Concurrent Request Tests**: Testet mehrere gleichzeitige API-Aufrufe
- **💡 Session-Management**: Wiederverwendung von HTTP-Verbindungen

## Beispiel-Verwendung

### cURL
```bash
curl -X POST "http://localhost:8082/YTtranscript" \
  -H "X-API-Key: dein-geheimer-api-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=8gHt3fwub7U", "languages": ["de", "en"]}'
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
    "url": "https://www.youtube.com/watch?v=8gHt3fwub7U",
    "languages": ["de", "en"]
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
    url: 'https://www.youtube.com/watch?v=8gHt3fwub7U',
    languages: ['de', 'en']
  })
});

const data = await response.json();
console.log(data);
```

### Python Asynchron (aiohttp)
```python
import asyncio
import aiohttp

async def test_api():
    async with aiohttp.ClientSession() as session:
        headers = {
            "X-API-Key": "dein-geheimer-api-key",
            "Content-Type": "application/json"
        }
        data = {
            "url": "https://www.youtube.com/watch?v=8gHt3fwub7U",
            "languages": ["de", "en"]
        }
        
        async with session.post(
            "http://localhost:8082/YTtranscript",
            headers=headers,
            json=data
        ) as response:
            result = await response.json()
            print(result)

# Ausführung
asyncio.run(test_api())
```

### Mehrere gleichzeitige Requests
```python
import asyncio
import aiohttp

async def concurrent_requests():
    async with aiohttp.ClientSession() as session:
        headers = {
            "X-API-Key": "dein-geheimer-api-key",
            "Content-Type": "application/json"
        }
        
        # Mehrere URLs gleichzeitig verarbeiten
        urls = [
            "https://www.youtube.com/watch?v=8gHt3fwub7U",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=example123"
        ]
        
        tasks = []
        for url in urls:
            data = {"url": url, "languages": ["de", "en"]}
            task = session.post(
                "http://localhost:8082/YTtranscript",
                headers=headers,
                json=data
            )
            tasks.append(task)
        
        # Alle Requests parallel ausführen
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                print(f"URL {i+1} failed: {response}")
            else:
                result = await response.json()
                print(f"URL {i+1} result: {result['video_url']}")

# Ausführung
asyncio.run(concurrent_requests())
```

## Performance & Asynchrone Features

### Asynchrone Test-Suite

Die `test_api_async.py` bietet erweiterte Test-Funktionalitäten:

#### Features:
- **Session-Management**: Wiederverwendung von HTTP-Verbindungen
- **Parallele Ausführung**: Alle Tests laufen gleichzeitig mit `asyncio.gather()`
- **Performance-Vergleich**: Direkte Gegenüberstellung parallel vs. sequenziell
- **Concurrent Request Tests**: Testet Verhalten bei gleichzeitigen API-Aufrufen
- **Detaillierte Metriken**: Ausführungszeiten für jeden einzelnen Test

#### Technische Details:
```python
# Async Context Manager für Session-Management
async with AsyncAPITester(BASE_URL, API_KEY) as tester:
    # Parallele Ausführung mit asyncio.gather()
    results = await asyncio.gather(*tasks, return_exceptions=True)
```

#### Connection Pool Konfiguration:
```python
self.session = aiohttp.ClientSession(
    timeout=aiohttp.ClientTimeout(total=30),
    connector=aiohttp.TCPConnector(limit=10)  # Max 10 gleichzeitige Verbindungen
)
```

### Performance-Metriken

Die asynchrone Version misst:
- **Execution Time**: Einzelne Test-Ausführungszeiten
- **Total Time**: Gesamtzeit für alle Tests
- **Speedup Factor**: Verbesserung durch parallele Ausführung
- **Requests per Second**: Bei Concurrent Request Tests
- **Success Rate**: Erfolgsrate bei gleichzeitigen Requests

### Beispiel-Output:
```
🚀 Starte parallele API-Tests...
🧪 Teste Root-Endpunkt...
✅ Status: 200
⏱️ Ausführungszeit: 0.15s

📊 Test-Zusammenfassung:
✅ Erfolgreich: 5/5
⏱️ Gesamtzeit: 2.34s
🚀 Parallel-Speedup: Tests liefen gleichzeitig!

🏆 Performance-Vergleich:
⚡ Parallel: 2.34s
🐌 Sequenziell: 8.92s
🚀 Speedup: 3.81x schneller
```

### Multithreading vs. Asyncio

Diese Implementierung nutzt **Asyncio** statt traditionellem Multithreading:

**Vorteile von Asyncio:**
- Kein Thread-Overhead
- Bessere Resource-Effizienz
- Einfachere Fehlerbehandlung
- Keine Race Conditions
- Skaliert besser bei I/O-intensiven Operationen

**Warum für API-Tests ideal:**
- HTTP-Requests sind I/O-gebunden
- Wartezeiten auf Server-Antworten können parallel überbrückt werden
- Session-Pooling reduziert Connection-Overhead
- Exception-Handling pro Request

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
├── requirements.txt         # Python-Dependencies (inkl. aiohttp)
├── start_server.py          # Server-Startskript
├── test_api.py             # Synchrone API-Tests
├── test_api_async.py       # Asynchrone API-Tests mit Multithreading
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