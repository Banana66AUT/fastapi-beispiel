from youtube_transcript_api import YouTubeTranscriptApi


class LoadTranscript:
    def __init__(self, url):
        self.url = url

    def run(self):
        video_id = self.url.split("v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = "\n".join([entry['text'] for entry in transcript])
        return {"transcript": full_text}