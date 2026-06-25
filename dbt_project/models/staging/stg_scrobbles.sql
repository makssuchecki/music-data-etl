{{ config(materialized="view") }}

select
    id  as scrobble_id,
    track_name,
    artist_name,
    album_name,
    scrobbled_at,
    mbid,
    ingested_at

from {{ source('raw', 'scrobbles') }}