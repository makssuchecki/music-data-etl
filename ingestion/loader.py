import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

from ingestion.lastfm.models import Scrobble

load_dotenv()

def get_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "music_dwh"),
        user=os.getenv("POSTGRES_USER", "music_user"),
        password=os.getenv("POSTGRES_PASSWORD", "music_password"),
    )

def load_scrobbles(scrobbles: list[Scrobble]) -> int:
    """Wstawia listę scrobble'ów do raw.scrobbles. Zwraca liczbę wstawionych wierszy"""
    if not scrobbles:
        return 0
    
    rows = [
        (s.track_name, s.artist_name, s.album_name, s.scrobbled_at, s.mbid)
        for s in scrobbles
    ]
    with get_conn() as conn, conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO raw.scrobbles
                (track_name, artist_name, album_name, scrobbled_at, mbid)
            VALUES %s
            ON CONFLICT DO NOTHING        
            """,
            rows,
        )
        return cur.rowcount