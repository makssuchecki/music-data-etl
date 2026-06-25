from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

DEFAULT_ARGS = {
    "owner": "music-etl",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

def ingest_scrobbles():
    import sys
    sys.path.insert(0, "/opt/airflow")

    from ingestion.lastfm.client import LastFmClient
    from ingestion.lastfm.extract import fetch_page
    from ingestion.loader import load_scrobbles

    client = LastFmClient()
    scrobbles = fetch_page(client, page=1)
    count = load_scrobbles(scrobbles)
    print(f"Załadowano {count} scrobble'ów")


with DAG(
    dag_id="music_etl_daily",
    description="Codzienny pipeline Last.fm → dbt",
    schedule="0 6 * * *",   # każdego dnia o 06:00 UTC
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=["music", "etl"],
) as dag:

    t_ingest = PythonOperator(
        task_id="ingest_scrobbles",
        python_callable=ingest_scrobbles,
    )

    t_dbt_staging = BashOperator(
        task_id="dbt_staging",
        bash_command="cd /opt/airflow/dbt_project && dbt run --select staging --profiles-dir /opt/airflow/dbt_project",
    )

    t_dbt_marts = BashOperator(
        task_id="dbt_marts",
        bash_command="cd /opt/airflow/dbt_project && dbt run --select marts --profiles-dir /opt/airflow/dbt_project",
    )

    t_dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt_project && dbt test --profiles-dir /opt/airflow/dbt_project",
    )

    t_ingest >> t_dbt_staging >> t_dbt_marts >> t_dbt_test