# Music Data Pipeline

End-to-end batch ELT pipeline for music listening data. (Last.fm API)

## Architecture

**Stack:** Python - dbt - PostgreSQL - Apache Airflow - Docker - GitHub Actions

## Data Model

Star schema built on top of Last.fm scrobble history:

| Table | Description |
| `raw.scrobbles` | Raw JSON landing zone from Last.fm API |
| `staging.stg_scrobbles` | Cleaned and typed scrobbles (dbt view) |
| `marts.dim_date` | Date dimension with calendar attributes |
| `marts.dim_artist` | Artist dimension with play counts |
| `marts.dim_track` | Track dimension derived from scrobble history |
| `marts.fact_scrobbles` | One row per scrobble event (incremental) |

## Pipeline

Airflow DAG `music_elt_daily` runs daily at 06:00 UTC:
ingest_scrobbles -> dbt_staging -> dbt_marts -> dbt_test

- **Retries:** 2 attempts with 5 minute delay
- **Data quality:** dbt tests on every run (not_null, unique, relationships)

## Quick Start

**Prerequisites:** Docker Desktop, Python 3.10+

```bash
git clone https://github.com/YOUR_USERNAME/music-data-elt.git
cd music-data-etl

cp .env.example .env
# Add your LASTFM_API_KEY and LASTFM_USERNAME to .env

docker compose up -d
```

## CI

GitHub Actions runs on every push to `main`:
- `ruff` linting
- `pytest` unit tests
- `dbt compile` against a test PostgreSQL instance
