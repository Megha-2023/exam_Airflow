import requests
import json
import os
from datetime import datetime
from airflow.models import Variable


def fetch_weather_data():
    """
    Task (1) — Retrieve current weather data from OpenWeatherMap for each
    city listed in the Airflow Variable 'cities' and save the raw response
    as a JSON file inside /app/raw_files/.
"""

    # --- 1. Fetch from environment variables -------------------------------------------
    cities = Variable.get("cities", default_var="paris,london,orleans").split(",")
    cities = [city.strip() for city in cities]
    api_key = Variable.get("openweather_api_key")

    # --- 2. Fetch data for every city ----------------------------------------
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    all_data = []
    for city in cities:
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
        }
        print(params)
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        all_data.append(response.json())
        print(f"[Task 1] Fetched data for '{city}' — HTTP {response.status_code}")

    # --- 3. Build output file path -------------------------------------------
    # Format: "YYYY-MM-DD HH:MM.json"
    filename = datetime.now().strftime("%Y-%m-%d %H:%M") + ".json"

    output_dir = "/app/raw_files"
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, filename)

    # --- 4. Write to disk ----------------------------------------------------
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    print(f"[Task 1] Saved {len(all_data)} cities → '{file_path}'")



fetch_weather_data()
