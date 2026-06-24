from datetime import datetime, timezone
from ingestion.lastfm.models import Scrobble
from ingestion.lastfm.client import LastFmClient


def parse_track(track: dict) -> Scrobble | None:
    """Zamienia surowy dict z API na model Scrobble. Zwraca None dla 'now playing'."""
    if track.get("@attr", {}).get("nowplaying"):
        return None

    date_info = track.get("date")
    if not date_info:
        return None

    return Scrobble(
        track_name=track["name"],
        artist_name=track["artist"]["#text"],
        album_name=track["album"]["#text"] or None,
        scrobbled_at=datetime.fromtimestamp(int(date_info["uts"]), tz=timezone.utc),
        mbid=track.get("mbid"),
    )


def fetch_page(client: LastFmClient, page: int) -> list[Scrobble]:
    """Pobiera jedną stronę scrobble'ów i zwraca listę modeli."""
    data = client.get_recent_tracks(page=page)
    tracks = data["recenttracks"]["track"]

    scrobbles = []
    for track in tracks:
        parsed = parse_track(track)
        if parsed:
            scrobbles.append(parsed)

    return scrobbles