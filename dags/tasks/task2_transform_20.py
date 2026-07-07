import os
import pandas as pd
from tasks.task3_transform_all import transform_data_into_csv


def transform_last_20_files():
    """
    Task (2) — Take the last 20 raw JSON files, concatenate and transform
    them into /app/clean_data/data.csv.
    Used by the dashboard to display the latest observations.
    """
    os.makedirs('/app/clean_data', exist_ok=True)
    transform_data_into_csv(n_files=20, filename='data.csv')
    print("[Task 2] data.csv created from last 20 files.")