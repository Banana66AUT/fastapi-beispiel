import requests
import json

# API-Konfiguration
BASE_URL = "http://localhost:8082"
API_KEY = "dein-geheimer-api-key"

def test_root_endpoint():
    """Teste den Root-Endpunkt"""
    print("🧪 Teste Root-Endpunkt...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_youtube_transcript():
    """Teste den YouTube-Transcript-Endpunkt"""
    print("🧪 Teste YouTube-Transcript-Endpunkt...")
    
    # Test-URL (kurzes Video)
    test_url = "https://www.youtube.com/watch?v=8gHt3fwub7U"
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "url": test_url
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/YTtranscript",
            headers=headers,
            json=data
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Video URL: {result['video_url']}")
            print(f"Transcript (erste 200 Zeichen): {result['transcript'][:200]}...")
        else:
            print(f"Fehler: {response.json()}")
            
    except Exception as e:
        print(f"Fehler beim Request: {e}")
    
    print()

def test_without_api_key():
    """Teste ohne API-Key (sollte 401 zurückgeben)"""
    print("🧪 Teste ohne API-Key...")
    
    data = {
        "url": "https://www.youtube.com/watch?v=8gHt3fwub7U"
    }
    
    response = requests.post(
        f"{BASE_URL}/YTtranscript",
        json=data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_invalid_url():
    """Teste mit ungültiger URL"""
    print("🧪 Teste mit ungültiger URL...")
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "url": "https://www.youtube.com/watch?v=invalid"
    }
    
    response = requests.post(
        f"{BASE_URL}/YTtranscript",
        headers=headers,
        json=data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == "__main__":
    print("🚀 Starte API-Tests...")
    print(f"Base URL: {BASE_URL}")
    print(f"API Key: {API_KEY}")
    print("=" * 50)
    
    try:
        test_root_endpoint()
        test_youtube_transcript()
        test_without_api_key()
        test_invalid_url()
        
        print("✅ Alle Tests abgeschlossen!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Fehler: Kann keine Verbindung zum Server herstellen.")
        print("Stelle sicher, dass der Server läuft: python start_server.py")
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}") 