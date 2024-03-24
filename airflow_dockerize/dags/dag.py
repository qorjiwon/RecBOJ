from datetime import timedelta,datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

import sys, os
sys.path.append(os.getcwd())

default_args = {
    'owner': 'DDing',
    'depends_on_past': False,
    'email': ['nme0529@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

dag_args = dict(
    dag_id="crawling-entire-user",
    default_args=default_args,
    description='RecBOJ',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 3, 21),
    tags=['recboj-airflow-test'],
)

with DAG( **dag_args ) as dag:
    start = BashOperator(
        task_id='start',
        bash_command='echo "start"',
    )

    update = BashOperator(
        task_id='update',
        bash_command= 'scrapy runspider probleminfo.py',
        cwd = '/opt/airflow/scrapy/recboj/recboj/spiders'
    )

    complete = BashOperator(
        task_id='complete_bash',
        bash_command='echo "complete"',
    )

    start >> update >> complete