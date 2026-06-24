import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
from ingestion.lastfm.models import Scrobble
from ingestion.lastfm.client import LastFmClient
from ingestion.lastfm.extract import fetch_page

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


client = LastFmClient()
total = client.get_total_pages()
print(f"\nMasz {total} stron scrobble'ów w Last.fm")

data = client.get_recent_tracks(limit=3)
tracks = data["recenttracks"]["track"]
print(f"Pobrano {len(tracks)} utworów przez klienta")


scrobbles = fetch_page(client, page=1)
print(f"\nPierwsza strona: {len(scrobbles)} scrobble'ów")
print("Przykład:")
s = scrobbles[0]
print(f"    {s.artist_name} - {s.track_name}")
print(f"    album: {s.album_name}")
print(f"    kiedy: {s.scrobbled_at}")
