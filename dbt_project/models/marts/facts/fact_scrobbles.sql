{{ config(
    materialized="incremental",
    unique_key="scrobble_id"
) }}

select
    s.scrobble_id,

    d.date_key,
    s.artist_name,
    s.track_name,
    s.album_name,

    s.scrobbled_at,
    extract(hour from s.scrobbled_at)::int      as hour_of_day,
    extract(dow from s.scrobbled_at)::int       as day_of_week,

    1                                           as play_count

from {{ ref('stg_scrobbles') }} s
left join {{ ref('dim_date') }} d
    on to_char(s.scrobbled_at at time zone 'UTC', 'YYYYMMDD')::int = d.date_key

{% if is_incremental() %}
where s.scrobbled_at > (select max(scrobbled_at) from {{ this }})
{% endif %}
