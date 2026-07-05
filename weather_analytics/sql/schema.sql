DROP SCHEMA IF EXISTS weather_analytics CASCADE;

CREATE SCHEMA weather_analytics;


CREATE TABLE weather_analytics.cities(
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL UNIQUE,
    longitude NUMERIC(8, 4) NOT NULL,
    latitude  NUMERIC(8, 4) NOT NULL
);


CREATE TABLE weather_analytics.weather(
    weather_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES weather_analytics.cities(city_id),
    weather_date DATE NOT NULL,
    max_temp NUMERIC(5, 2),
    min_temp NUMERIC(5, 2),
    max_apparent_temp NUMERIC(5, 2),
    min_apparent_temp NUMERIC(5, 2),
    max_wind_speed NUMERIC(5, 2),
    precipitation NUMERIC(5, 2),
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    UNIQUE (city_id, weather_date)    
);


CREATE TABLE weather_analytics.forecast(
    forecast_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES weather_analytics.cities(city_id),
    record_date DATE NOT NULL,
    retrieved_on DATE NOT NULL,
    max_temp NUMERIC(5, 2),
    min_temp NUMERIC(5, 2),
    max_apparent_temp NUMERIC(5, 2),
    min_apparent_temp NUMERIC(5, 2),
    max_wind_speed NUMERIC(5, 2),
    precipitation NUMERIC(5, 2),
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    UNIQUE (city_id, record_date, retrieved_on)
);
