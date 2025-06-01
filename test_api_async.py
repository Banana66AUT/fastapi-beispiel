import asyncio
import aiohttp
import json
import time
from typing import List, Dict, Any

# API-Konfiguration
BASE_URL = "http://localhost:8082"
API_KEY = "dein-geheimer-api-key"

class AsyncAPITester:
    """Asynchroner API-Tester mit Session-Management und paralleler Ausführung"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.session = None
        
    async def __aenter__(self):
        """Async Context Manager - erstellt HTTP-Session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(limit=10)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async Context Manager - schließt HTTP-Session"""
        if self.session:
            await self.session.close()

    async def test_root_endpoint(self) -> Dict[str, Any]:
        """Teste den Root-Endpunkt asynchron"""
        print("🧪 Teste Root-Endpunkt...")
        start_time = time.time()
        
        try:
            async with self.session.get(f"{self.base_url}/") as response:
                status = response.status
                data = await response.json()
                execution_time = time.time() - start_time
                
                print(f"✅ Status: {status}")
                print(f"Response: {data}")
                print(f"⏱️ Ausführungszeit: {execution_time:.2f}s")
                print()
                
                return {
                    "test": "root_endpoint",
                    "status": status,
                    "success": status == 200,
                    "execution_time": execution_time,
                    "response": data
                }
                
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Fehler beim Root-Endpunkt: {e}")
            print(f"⏱️ Ausführungszeit: {execution_time:.2f}s")
            print()
            
            return {
                "test": "root_endpoint",
                "status": None,
                "success": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def test_youtube_transcript(self) -> Dict[str, Any]:
        """Teste den YouTube-Transcript-Endpunkt asynchron"""
        print("🧪 Teste YouTube-Transcript-Endpunkt...")
        start_time = time.time()
        
        # Test-URL (kurzes Video)
        test_url = "https://www.youtube.com/watch?v=8gHt3fwub7U"
        
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "url": test_url
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/YTtranscript",
                headers=headers,
                json=data
            ) as response:
                status = response.status
                result = await response.json()
                execution_time = time.time() - start_time
                
                print(f"✅ Status: {status}")
                
                if status == 200:
                    print(f"Video URL: {result['video_url']}")
                    print(f"Transcript (erste 200 Zeichen): {result['transcript'][:200]}...")
                else:
                    print(f"Fehler: {result}")
                
                print(f"⏱️ Ausführungszeit: {execution_time:.2f}s")
                print()
                
                return {
                    "test": "youtube_transcript",
                    "status": status,
                    "success": status == 200,
                    "execution_time": execution_time,
                    "response": result
                }
                
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Fehler beim YouTube-Transcript-Test: {e}")
            print(f"⏱️ Ausführungszeit: {execution_time:.2f}s")
            print()
            
            return {
                "test": "youtube_transcript",
                "status": None,
                "success": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def test_without_api_key(self) -> Dict[str, Any]:
        """Teste ohne API-Key (sollte 401 zurückgeben)"""
        print("🧪 Teste ohne API-Key...")
        start_time = time.time()
        
        data = {
            "url": "https://www.youtube.com/watch?v=8gHt3fwub7U"
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/YTtranscript",
                json=data
            ) as response:
                status = response.status
                result = await response.json()
                execution_time = time.time() - start_time
                
                print(f"✅ Status: {status}")
                print(f"Response: {result}")
                print(f"⏱️ Ausführungszeit: {execution_time:.2f}s")
                print()
                
                return {
                    "test": "without_api_key",
                    "status": status,
                    "success": status == 401,  # Erwarten 401 Unauthorized
                    "execution_time": execution_time,
                    "response": result
                }
                
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Fehler beim Test ohne API-Key: {e}")
            print(f"⏱️ Ausführungszeit: {execution_time:.2f}s")
            print()
            
            return {
                "test": "without_api_key",
                "status": None,
                "success": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def test_invalid_url(self) -> Dict[str, Any]:
        """Teste mit ungültiger URL"""
        print("🧪 Teste mit ungültiger URL...")
        start_time = time.time()
        
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "url": "https://www.youtube.com/watch?v=invalid"
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/YTtranscript",
                headers=headers,
                json=data
            ) as response:
                status = response.status
                result = await response.json()
                execution_time = time.time() - start_time
                
                print(f"✅ Status: {status}")
                print(f"Response: {result}")
                print(f"⏱️ Ausführungszeit: {execution_time:.2f}s")
                print()
                
                return {
                    "test": "invalid_url",
                    "status": status,
                    "success": status == 400,  # Erwarten 400 Bad Request
                    "execution_time": execution_time,
                    "response": result
                }
                
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Fehler beim Test mit ungültiger URL: {e}")
            print(f"⏱️ Ausführungszeit: {execution_time:.2f}s")
            print()
            
            return {
                "test": "invalid_url",
                "status": None,
                "success": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def test_multiple_concurrent_requests(self, num_requests: int = 5) -> Dict[str, Any]:
        """Teste mehrere gleichzeitige Requests zum gleichen Endpunkt"""
        print(f"🧪 Teste {num_requests} gleichzeitige Requests...")
        start_time = time.time()
        
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "url": "https://www.youtube.com/watch?v=8gHt3fwub7U"
        }
        
        # Erstelle Tasks für gleichzeitige Requests
        tasks = []
        for i in range(num_requests):
            task = self._single_request(f"request_{i+1}", headers, data)
            tasks.append(task)
        
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            execution_time = time.time() - start_time
            
            successful_requests = 0
            for result in results:
                if isinstance(result, dict) and result.get("success", False):
                    successful_requests += 1
            
            print(f"✅ {successful_requests}/{num_requests} Requests erfolgreich")
            print(f"⏱️ Gesamtzeit für {num_requests} Requests: {execution_time:.2f}s")
            print(f"📊 Durchschnitt pro Request: {execution_time/num_requests:.2f}s")
            print()
            
            return {
                "test": "concurrent_requests",
                "total_requests": num_requests,
                "successful_requests": successful_requests,
                "success": successful_requests == num_requests,
                "execution_time": execution_time,
                "average_per_request": execution_time / num_requests,
                "results": results
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Fehler bei gleichzeitigen Requests: {e}")
            print(f"⏱️ Ausführungszeit: {execution_time:.2f}s")
            print()
            
            return {
                "test": "concurrent_requests",
                "total_requests": num_requests,
                "successful_requests": 0,
                "success": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def _single_request(self, request_id: str, headers: dict, data: dict) -> Dict[str, Any]:
        """Hilfsfunktion für einzelne Requests"""
        try:
            async with self.session.post(
                f"{self.base_url}/YTtranscript",
                headers=headers,
                json=data
            ) as response:
                status = response.status
                result = await response.json()
                
                return {
                    "request_id": request_id,
                    "status": status,
                    "success": status == 200,
                    "response": result
                }
                
        except Exception as e:
            return {
                "request_id": request_id,
                "status": None,
                "success": False,
                "error": str(e)
            }

    async def run_all_tests_parallel(self) -> Dict[str, Any]:
        """Führe alle Tests parallel aus"""
        print("🚀 Starte parallele API-Tests...")
        print(f"Base URL: {self.base_url}")
        print(f"API Key: {self.api_key}")
        print("=" * 50)
        
        start_time = time.time()
        
        # Führe alle Tests parallel aus
        tasks = [
            self.test_root_endpoint(),
            self.test_youtube_transcript(),
            self.test_without_api_key(),
            self.test_invalid_url(),
            self.test_multiple_concurrent_requests(3)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        # Verarbeite Ergebnisse
        test_results = []
        successful_tests = 0
        
        for result in results:
            if isinstance(result, Exception):
                test_results.append({
                    "test": "unknown",
                    "success": False,
                    "error": str(result)
                })
            else:
                test_results.append(result)
                if result.get("success", False):
                    successful_tests += 1
        
        # Zusammenfassung
        summary = {
            "total_tests": len(test_results),
            "successful_tests": successful_tests,
            "failed_tests": len(test_results) - successful_tests,
            "total_execution_time": total_time,
            "results": test_results
        }
        
        print("=" * 50)
        print("📊 Test-Zusammenfassung:")
        print(f"✅ Erfolgreich: {successful_tests}/{len(test_results)}")
        print(f"❌ Fehlgeschlagen: {len(test_results) - successful_tests}/{len(test_results)}")
        print(f"⏱️ Gesamtzeit: {total_time:.2f}s")
        print(f"🚀 Parallel-Speedup: Tests liefen gleichzeitig!")
        
        return summary

    async def run_all_tests_sequential(self) -> Dict[str, Any]:
        """Führe alle Tests sequenziell aus (zum Vergleich)"""
        print("🐌 Starte sequenzielle API-Tests...")
        print(f"Base URL: {self.base_url}")
        print(f"API Key: {self.api_key}")
        print("=" * 50)
        
        start_time = time.time()
        
        # Führe alle Tests nacheinander aus
        test_functions = [
            self.test_root_endpoint,
            self.test_youtube_transcript,
            self.test_without_api_key,
            self.test_invalid_url,
            lambda: self.test_multiple_concurrent_requests(3)
        ]
        
        results = []
        successful_tests = 0
        
        for test_func in test_functions:
            try:
                result = await test_func()
                results.append(result)
                if result.get("success", False):
                    successful_tests += 1
            except Exception as e:
                results.append({
                    "test": test_func.__name__,
                    "success": False,
                    "error": str(e)
                })
        
        total_time = time.time() - start_time
        
        # Zusammenfassung
        summary = {
            "total_tests": len(results),
            "successful_tests": successful_tests,
            "failed_tests": len(results) - successful_tests,
            "total_execution_time": total_time,
            "results": results
        }
        
        print("=" * 50)
        print("📊 Test-Zusammenfassung (Sequenziell):")
        print(f"✅ Erfolgreich: {successful_tests}/{len(results)}")
        print(f"❌ Fehlgeschlagen: {len(results) - successful_tests}/{len(results)}")
        print(f"⏱️ Gesamtzeit: {total_time:.2f}s")
        
        return summary


async def main():
    """Hauptfunktion für die asynchrone Ausführung"""
    try:
        async with AsyncAPITester(BASE_URL, API_KEY) as tester:
            # Führe Tests parallel aus
            parallel_results = await tester.run_all_tests_parallel()
            
            print("\n" + "=" * 70)
            print("🔄 Zum Vergleich: Sequenzielle Ausführung...")
            print("=" * 70)
            
            # Führe Tests sequenziell aus (zum Vergleich)
            sequential_results = await tester.run_all_tests_sequential()
            
            # Performance-Vergleich
            parallel_time = parallel_results["total_execution_time"]
            sequential_time = sequential_results["total_execution_time"]
            speedup = sequential_time / parallel_time if parallel_time > 0 else 1
            
            print("\n" + "=" * 70)
            print("🏆 Performance-Vergleich:")
            print(f"⚡ Parallel: {parallel_time:.2f}s")
            print(f"🐌 Sequenziell: {sequential_time:.2f}s")
            print(f"🚀 Speedup: {speedup:.2f}x schneller")
            print("=" * 70)
            
        print("✅ Alle Tests abgeschlossen!")
        
    except aiohttp.ClientConnectorError:
        print("❌ Fehler: Kann keine Verbindung zum Server herstellen.")
        print("Stelle sicher, dass der Server läuft: python start_server.py")
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")


if __name__ == "__main__":
    # Führe die asynchrone main-Funktion aus
    asyncio.run(main()) 