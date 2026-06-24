CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.scrobbles (
    id          BIGSERIAL PRIMARY KEY,
    track_name  TEXT        NOT NULL,
    artist_name TEXT        NOT NULL,
    album_name  TEXT,
    scrobbled_at TIMESTAMPTZ NOT NULL,
    mbid        TEXT,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_scrobbles_scrobbled_at
    ON raw.scrobbles(scrobbled_at);