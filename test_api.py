import requests
from dotenv import load_dotenv
import os
from ingestion.lastfm.models import Scrobble
from datetime import datetime, timezone

load_dotenv()

API_KEY = os.getenv("LASTFM_API_KEY")
USERNAME = os.getenv("LASTFM_USERNAME")

response = requests.get("https://ws.audioscrobbler.com/2.0/", params={
    "method": "user.getRecentTracks",
    "user": USERNAME,
    "api_key": API_KEY,
    "format": "json",
    "limit": 5,
})

data = response.json()

tracks = data["recenttracks"]["track"]
print(f"Ostatnie 5 utworów dla {USERNAME}:\n")
for track in tracks:
    if isinstance(track.get("date"), dict):
        print(f"  {track['artist']['#text']} — {track['name']}  ({track['date']['#text']})")

test = Scrobble(
    track_name="Bohemian Rhapsody",
    artist_name="Queen",
    scrobbled_at=datetime(2024, 1, 1, 21, 0, tzinfo=timezone.utc),
)
print(f"\nModel działa: {test.artist_name} — {test.track_name}")
print(f"album_name pusty = None: {test.album_name}")