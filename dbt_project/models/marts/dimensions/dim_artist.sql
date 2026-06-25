{{ config(materialized="table") }}

select
    artist_name,
    count(*)                            as total_scrobbles,
    min(scrobbled_at)                   as first_scrobbled_at,
    max(scrobbled_at)                   as last_scrobbled_at,
    count(distinct date(scrobbled_at))  as days_listened

from {{ ref('stg_scrobbles')}}

group by artist_name