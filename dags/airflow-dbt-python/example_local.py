import datetime as dt

import pendulum
from airflow import DAG
from airflow_dbt_python.operators.dbt import DbtRunOperator

from include.profiles import airflow_db
from include.constants import jaffle_shop_path, venv_execution_config


with DAG(
    dag_id="example_local",
    schedule_interval="0 0 * * *",
    start_date=pendulum.today("UTC").add(days=-1),
    catchup=False,
    dagrun_timeout=dt.timedelta(minutes=60),
) as dag:
    dbt_run = DbtRunOperator(
        task_id="dbt_python_run_daily",
        project_dir=jaffle_shop_path,
        profiles_dir="~/.dbt/",
        select=["+tag:daily"],
        exclude=["tag:deprecated"],
        target="production",
        profile="my-project",
    )
