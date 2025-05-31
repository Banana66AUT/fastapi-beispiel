from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


class LoadTranscript:
    def __init__(self, url, language_codes=None):
        self.url = url
        # Fallback-Sprachen: Deutsch, Englisch, dann alle verfügbaren
        self.language_codes = language_codes or ['de', 'en']

    def run(self):
        video_id = self.url.split("v=")[1]
        
        try:
            # Versuche zuerst mit bevorzugten Sprachen
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=self.language_codes)
            full_text = "\n".join([entry['text'] for entry in transcript])
            used_language = self._get_used_language(video_id)
            
            return {
                "transcript": full_text,
                "language": used_language,
                "video_id": video_id
            }
            
        except NoTranscriptFound:
            # Falls keine bevorzugten Sprachen verfügbar sind, nimm die erste verfügbare
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                # Nimm das erste verfügbare Transcript
                transcript = transcript_list.find_transcript([]).fetch()
                full_text = "\n".join([entry['text'] for entry in transcript])
                
                return {
                    "transcript": full_text,
                    "language": "auto-detected",
                    "video_id": video_id
                }
            except Exception as e:
                # Liste verfügbare Sprachen für bessere Fehlermeldung
                available_languages = self._get_available_languages(video_id)
                raise Exception(f"Kein Transcript verfügbar. Verfügbare Sprachen: {available_languages}")
        
        except TranscriptsDisabled:
            raise Exception("Transcripts sind für dieses Video deaktiviert")
        
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen des Transcripts: {str(e)}")
    
    def _get_used_language(self, video_id):
        """Ermittelt die verwendete Sprache"""
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            for language_code in self.language_codes:
                try:
                    transcript = transcript_list.find_transcript([language_code])
                    return f"{language_code} ({transcript.language})"
                except:
                    continue
            return "unbekannt"
        except:
            return "unbekannt"
    
    def _get_available_languages(self, video_id):
        """Liste verfügbare Sprachen für bessere Fehlermeldung"""
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            languages = []
            for transcript in transcript_list:
                languages.append(f"{transcript.language_code} ({transcript.language})")
            return languages
        except:
            return ["Keine verfügbar"]