import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://ws.audioscrobbler.com/2.0/"

class LastFmClient:
    def __init__(self):
        self.api_key = os.getenv("LASTFM_API_KEY")
        self.username = os.getenv("LASTFM_USERNAME")
        self._last_call = 0.0

    def _get(self, method, **params):
        """Bazowa metoda — dodaje klucz, format, i pilnuje rate limit."""
        elapsed = time.time() - self._last_call
        if elapsed < 0.2:
            time.sleep(0.2 - elapsed)

        response = requests.get(BASE_URL, params={
            "method": method,
            "api_key": self.api_key,
            "format": "json",
            **params,
        }, timeout=10)

        response.raise_for_status()
        self._last_call = time.time()

        data =response.json()
        if "error" in data:
            raise ValueError(f"Last.fm error {data['error']}: {data['message']}")
        return data
    
    def get_recent_tracks(self, page=1, limit=200):
        """Pobiera ostatnie scrobble użytkownika"""
        return self._get(
            "user.getRecentTracks",
            user=self.username,
            limit=limit,
            page=page,
        )
    
    def get_total_pages(self):
        """Sprawdza ile stron scrobble'ów ma użytkownik."""
        data = self.get_recent_tracks(limit=1)
        return int(data["recenttracks"]["@attr"]["totalPages"])