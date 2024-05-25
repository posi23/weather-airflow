import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import json
import sys
sys.path.insert(0, '/opt/airflow/etl')
from transform_data import transform_weather_data, save_to_s3

weathermap_api_key = os.environ.get('WEATHERMAP_API_KEY')

default_args = {
    'owner': 'posi',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'weather_dag',
    default_args=default_args,
    description='A simple weather DAG',
    schedule_interval='@daily',
    catchup=False,
) as dag:
    

    is_api_ready = HttpSensor(
        task_id='is_api_ready',
        http_conn_id='weathermap_api',
        endpoint=f'/data/2.5/weather?q=Calgary&appid={weathermap_api_key}'
    )

    extract_weather_data = SimpleHttpOperator(
        task_id='extract_weather_data',
        http_conn_id='weathermap_api',
        method='GET',
        endpoint=f'/data/2.5/weather?q=Calgary&appid={weathermap_api_key}',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    transform_weather_data = PythonOperator(
        task_id='transform_weather_data',
        python_callable=transform_weather_data,
    )

    save_to_s3 = PythonOperator(
        task_id='save_to_s3',
        python_callable=save_to_s3,
    )

    is_api_ready >> extract_weather_data >> transform_weather_data >> save_to_s3