{{ config(materialized="table") }}

with date_series as (
    select generate_series(
        '2010-01-01'::date,
        current_date + interval '1 year',
        '1 day'::interval
    )::date as full_date
)

select
    to_char(full_date, 'YYYYMMDD')::int     as date_key,
    full_date,
    extract(year from full_date)::int        as year,
    extract(quarter from full_date)::int     as quarter,
    extract(month from full_date)::int       as month,
    to_char(full_date, 'TMMonth')            as month_name,
    extract(week from full_date)::int        as week_of_year,
    extract(dow from full_date)::int         as day_of_week,
    to_char(full_date, 'TMDay')              as day_name,
    case
        when extract(dow from full_date) in (0, 6) then true
        else false
    end                                      as is_weekend

from date_series