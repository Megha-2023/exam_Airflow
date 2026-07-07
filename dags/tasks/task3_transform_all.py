import os
import json
import pandas as pd


def transform_data_into_csv(n_files=None, filename='data.csv'):
    parent_folder = '/app/raw_files'
    files = sorted(os.listdir(parent_folder), reverse=True)
    if n_files:
        files = files[:n_files]

    dfs = []

    for f in files:
        with open(os.path.join(parent_folder, f), 'r') as file:
            data_temp = json.load(file)
        for data_city in data_temp:
            dfs.append(
                {
                    'temperature': data_city['main']['temp'],
                    'city': data_city['name'],
                    'pression': data_city['main']['pressure'],
                    'date': f.split('.')[0]
                }
            )

    df = pd.DataFrame(dfs)

    print('\n', df.head(10))

    df.to_csv(os.path.join('/app/clean_data', filename), index=False)


def transform_all_files():
    """
    Task (3) — Take ALL raw JSON files in /app/raw_files, concatenate and
    transform them into /app/clean_data/fulldata.csv.
    Used downstream in the DAG to train the ML model.
    """
    os.makedirs('/app/clean_data', exist_ok=True)
    transform_data_into_csv(n_files=None, filename='fulldata.csv')
    print("[Task 3] fulldata.csv created from all available files.")