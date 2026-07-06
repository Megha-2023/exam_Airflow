from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from tasks.task1_fetch import fetch_weather_data
# from tasks.task_2_transform_20 import transform_last_20_files
# from tasks.task_3_transform_all import transform_all_files
# Uncomment as you build each task:
# from weather_tasks.task_4_... import ...
# from weather_tasks.task_5_... import ...

with DAG(
    dag_id="weather_pipeline",
    description="Fetch OpenWeatherMap data, transform and load it",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
    tags=["weather", "openweathermap", "megha"],
) as dag:

    t1 = PythonOperator(
        task_id="fetch_weather_data",           # Task (1)
        python_callable=fetch_weather_data,
    )

   # t2 = PythonOperator(
   #     task_id="transform_last_20_files",      # Task (2) → data.csv (dashboard)
   #     python_callable=transform_last_20_files,
   # )

    #t3 = PythonOperator(
    #    task_id="transform_all_files",          # Task (3) → fulldata.csv (ML training)
    #   python_callable=transform_all_files,
    #)

    # Wire up future tasks below as you complete them:
    # t4 = PythonOperator(task_id="...", python_callable=...)
    # t5 = PythonOperator(task_id="...", python_callable=...)

    # t1 triggers both t2 and t3 in parallel, then future tasks follow t3
    t1 # >> [t2, t3]
    # t3 >> t4 >> t5