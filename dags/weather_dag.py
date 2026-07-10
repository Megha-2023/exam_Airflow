from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from tasks.task1_fetch import fetch_weather_data
from tasks.task2_transform_20 import transform_last_20_files
from tasks.task3_transform_all import transform_all_files
from tasks.task4_train_models import train_and_evaluate_model
from tasks.task5_select_model import select_and_save_best_model

with DAG(
    dag_id="weather_pipeline",
    description="Fetch OpenWeatherMap data, transform and load it",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
    tags=["weather", "openweathermap", "megha"],
) as dag:

    t1 = PythonOperator(
        task_id="fetch_weather_data",
        python_callable=fetch_weather_data,
    )

    t2 = PythonOperator(
       task_id="transform_last_20_files",
       python_callable=transform_last_20_files,
    )

    t3 = PythonOperator(
       task_id="transform_all_files",
       python_callable=transform_all_files,
    )

    t4a = PythonOperator(
        task_id="train_linear_regression",
        python_callable=train_and_evaluate_model,
        op_kwargs={'model': LinearRegression()},
    )

    t4b = PythonOperator(
        task_id="train_decision_tree",
        python_callable=train_and_evaluate_model,
        op_kwargs={'model': DecisionTreeRegressor()},
    )

    t4c = PythonOperator(
        task_id="train_random_forest",
        python_callable=train_and_evaluate_model,
        op_kwargs={'model': RandomForestRegressor()},
    )

    t5 = PythonOperator(
        task_id="select_best_model",
        python_callable=select_and_save_best_model,

    )
    # t1 triggers both t2 and t3 in parallel, then future tasks follow t3
    t1 >> [t2, t3]
    t3 >> [t4a, t4b, t4c]
    [t4a, t4b, t4c] >> t5
