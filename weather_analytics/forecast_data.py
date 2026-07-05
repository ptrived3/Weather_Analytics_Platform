import requests
import json
import os
from datetime import date

CITIES = {
    "San Francisco": {"latitude": 37.7749, "longitude": -122.4194},
    "Mesa":          {"latitude": 33.4223, "longitude": -111.8226},
    "Seattle":       {"latitude": 47.6062, "longitude": -122.3321},
}


FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
DAILY_VARS = "temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,precipitation_sum,wind_speed_10m_max"

def fetch_data(city_name, coordinates):
    params = {
        "latitude" : coordinates["latitude"],
        "longitude" : coordinates["longitude"],
        "forecast_days": 7,
        "daily": DAILY_VARS,
        "timezone": "America/Los_Angeles",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
    }
    response = requests.get(FORECAST_URL, params=params)
    response.raise_for_status()
    return response.json()


def main():

    os.makedirs("data", exist_ok=True)      # check if the data folder exists

    for city_name, coordinates in CITIES.items():
        print(f"Fetching {city_name}...")

        data = fetch_data(city_name, coordinates)
        data["retrieved_on"] = date.today().isoformat()

        filename = "data/raw_forecast_" + city_name.lower().replace(" ", "_") + ".json"       # give the JSON file a name

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        total_days = len(data["daily"]["time"])
        print(f"Saved {total_days} days to {filename}")
 
    print("Done!")



if __name__ == "__main__":
    main()
