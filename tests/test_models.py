from datetime import datetime, timezone
from ingestion.lastfm.models import Scrobble
from ingestion.lastfm.extract import parse_track


def test_scrobble_model():
    s = Scrobble(
        track_name="Bohemian Rhapsody",
        artist_name="Queen",
        scrobbled_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    assert s.track_name == "Bohemian Rhapsody"
    assert s.album_name is None
    assert s.mbid is None


def test_parse_track_skips_now_playing():
    track = {
        "@attr": {"nowplaying": "true"},
        "name": "Some Song",
        "artist": {"#text": "Some Artist"},
        "album": {"#text": ""},
        "date": {"uts": "1700000000"},
    }
    assert parse_track(track) is None


def test_parse_track_returns_scrobble():
    track = {
        "name": "Creep",
        "artist": {"#text": "Radiohead"},
        "album": {"#text": "Pablo Honey"},
        "mbid": "",
        "date": {"uts": "1700000000"},
    }
    result = parse_track(track)
    assert result is not None
    assert result.track_name == "Creep"
    assert result.artist_name == "Radiohead"
    assert result.mbid is None