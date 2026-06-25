{{ config(materialized="table") }}

SELECT
    track_name,
    artist_name,
    album_name,
    count(*)            as total_scrobbles,
    min(scrobbled_at)   as first_scrobbled_at,
    max(scrobbled_at)   as last_scrobbled_at

from {{ ref('stg_scrobbles') }}

group by track_name, artist_name, album_name