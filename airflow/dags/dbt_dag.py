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

dag = DAG('dbt_dag', default_args=default_args, schedule=timedelta(days=1))

run_snapshot_bronze = BashOperator(
    task_id='run_snapshot_bronze',
    bash_command='source /home/gaute/WOW_Auction_house_project/.venv/bin/activate && dbt snapshot --project-dir /home/gaute/WOW_Auction_house_project/dbt_WoW_Auction_House --select auction_house_api_snapshot',
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

run_dbt_bronze = BashOperator(
    task_id='run_dbt_bronze',
    bash_command='source /home/gaute/WOW_Auction_house_project/.venv/bin/activate && dbt run --project-dir /home/gaute/WOW_Auction_house_project/dbt_WoW_Auction_House --select deserialization',
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

run_dbt_silver= BashOperator(
    task_id='run_dbt_silver',
    bash_command='source /home/gaute/WOW_Auction_house_project/.venv/bin/activate && dbt run --project-dir /home/gaute/WOW_Auction_house_project/dbt_WoW_Auction_House --select marts.silver.*',
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

run_snapshot_silver = BashOperator(
    task_id='run_snapshot_silver',
    bash_command='source /home/gaute/WOW_Auction_house_project/.venv/bin/activate && dbt snapshot --project-dir /home/gaute/WOW_Auction_house_project/dbt_WoW_Auction_House --select flat_auction_snapshot',
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

run_dbt_gold= BashOperator(
    task_id='run_dbt_gold',
    bash_command='source /home/gaute/WOW_Auction_house_project/.venv/bin/activate && dbt run --project-dir /home/gaute/WOW_Auction_house_project/dbt_WoW_Auction_House --select marts.gold.*',
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

run_snapshot_gold = BashOperator(
    task_id='run_snapshot_gold',
    bash_command='source /home/gaute/WOW_Auction_house_project/.venv/bin/activate && dbt snapshot --project-dir /home/gaute/WOW_Auction_house_project/dbt_WoW_Auction_House --select g_pet_split_snapshot g_auction_split_snapshot',
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

run_snapshot_bronze >> run_dbt_bronze >> run_dbt_silver >> run_snapshot_silver >> run_dbt_gold >> run_snapshot_gold