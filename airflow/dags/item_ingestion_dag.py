from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 1),
    'retries': 1,
}

dag = DAG('item_ingestion_dag', default_args=default_args, schedule=timedelta(days=30))

run_python_ingestion = BashOperator(
    task_id='run_python_ingestion',
    bash_command='source /home/gaute/WOW_Auction_house_project/.venv/bin/activate && python3 /home/gaute/WOW_Auction_house_project/ingestion/item_api_call.py',
    dag=dag
)

run_snapshot_item = BashOperator(
    task_id='run_snapshot_item',
    bash_command='source /home/gaute/WOW_Auction_house_project/.venv/bin/activate && dbt snapshot --project-dir /home/gaute/WOW_Auction_house_project/dbt_WoW_Auction_House --select g_item_snapshot',
    env={
        'DBT_ACCOUNT': Variable.get('DBT_ACCOUNT'),
        'DBT_DATABASE': Variable.get('DBT_DATABASE'),
        'DBT_PASSWORD': Variable.get('DBT_PASSWORD'),
        'DBT_USER': Variable.get('DBT_USER'),
        'DBT_SCHEMA': Variable.get('DBT_SCHEMA'),
        'DBT_WAREHOUSE': Variable.get('DBT_WAREHOUSE'),
        'DBT_ROLE': Variable.get('DBT_ROLE'),
    },
    dag=dag
)

run_python_ingestion >> run_snapshot_item

