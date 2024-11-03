from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

from include.constants import jaffle_shop_path

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('dbt_bash', default_args=default_args, schedule_interval=timedelta(days=1))

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='cd ' + jaffle_shop_path + ' && dbt run',
    dag=dag,
)
