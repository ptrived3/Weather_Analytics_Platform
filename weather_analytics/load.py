import os
import psycopg
import pandas as pd
from dotenv import load_dotenv

# Load the variables from .env into the environment
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

CITY_INFO = {
    "San Francisco": (37.7749, -122.4194),
    "Mesa":          (33.4223, -111.8226),
    "Seattle":       (47.6062, -122.3321),
}


def insert_cities(cursor):
    """
    insert 3 cities
    return {city name : city id} for translation
    """

    city_ids = {}

    for name, (lat, lon) in CITY_INFO.items():
        cursor.execute(
            """
            INSERT INTO weather_analytics.cities (city_name, latitude, longitude)
            VALUES (%s, %s, %s)
            RETURNING city_id;
            """,
            (name, lat, lon,),
        )
    
        new_id = cursor.fetchone()[0]
        city_ids[name] = new_id

    print(f"Inserted {len(city_ids.keys())} cities.")
    print(f"(cities inserted: {city_ids})")

    return city_ids


def insert_weather(cursor, city_ids):
    df = pd.read_csv("data/cleaned_historical.csv")

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO weather_analytics.weather
            (city_id, weather_date, max_temp, min_temp, max_apparent_temp, 
            min_apparent_temp, max_wind_speed, precipitation, sunrise, sunset)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                city_ids[row["city_name"]],
                row["time"],
                row["temperature_2m_max"],
                row["temperature_2m_min"],
                row["apparent_temperature_max"],
                row["apparent_temperature_min"],
                row["wind_speed_10m_max"],
                row["precipitation_sum"],
                row["sunrise"],
                row["sunset"],                
            ),
        )

    print(f"Inserted {len(df)} weather rows for historical data.")

def insert_forecast(cursor, city_ids):
    df = pd.read_csv("data/cleaned_forecast.csv")

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO weather_analytics.forecast
            (city_id, record_date, retrieved_on, max_temp, min_temp, max_apparent_temp, 
            min_apparent_temp, max_wind_speed, precipitation, sunrise, sunset)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                city_ids[row["city_name"]],
                row["time"],
                row["retrieved_on"],
                row["temperature_2m_max"],
                row["temperature_2m_min"],
                row["apparent_temperature_max"],
                row["apparent_temperature_min"],
                row["wind_speed_10m_max"],
                row["precipitation_sum"],
                row["sunrise"],
                row["sunset"],
            ),
        )
    print("Inserted", len(df), "forecast rows")


def main():
    # open the connection and the cursor

    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()

    city_ids = insert_cities(cursor)
    insert_weather(cursor, city_ids)
    insert_forecast(cursor, city_ids)

    conn.commit()

    cursor.close()
    conn.close()
    print("Completed loading data")


if __name__ == "__main__":
    main()