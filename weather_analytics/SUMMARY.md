# Project Summary: Weather Analytics Pipeline
Author : Prachi Trivedi

## Cities and Date Range

This pipeline collects daily historical weather data for three U.S. cities chosen
for their contrasting climates: **San Francisco, CA** (mild coastal), **Mesa, AZ**
(desert), and **Seattle, WA** (cool and rainy). The contrast is intentional, it
lets the analytical queries surface meaningful differences rather than near-identical
numbers.

The historical data covers the full **2025 calendar year (2025-01-01 to 2025-12-31)**,
pulled from the Open-Meteo Archive API. A full year was chosen so that time-based
queries such as "hottest month" and "windiest week" have a complete range to compare
against. This produced **1,095 records** (365 days × 3 cities).

As a bonus, the pipeline also pulls a **7-day forecast** for each city from the
Open-Meteo Forecast API and stores it in a separate table. Because a forecast for a
given date is revised each day, forecast records are keyed by *when* the forecast was
retrieved (`retrieved_on`), so predictions are never confused with settled historical
observations.

## Data Quality Issues Encountered

The source data returned complete and clean. Profiling the 1,095 historical records
found:

- **Zero null values** across all columns
- **Zero duplicate (city, date) records**
- **All values within physically plausible ranges** (temperatures spanned 34.6°F to
  115.7°F across the three cities, consistent with their distinct climates)

No rows required removal during cleaning.

## How Issues Were Resolved

Although this particular data pull required no corrections, the pipeline is built to
defend against common data quality problems for future runs where the data may not be
as clean:

- **Profiling** (`profile_clean.py`) reports null counts, column types, value ranges,
  and duplicate (city, date) records before any changes are made.
- **Cleaning** converts date and timestamp columns to proper types, coerces metric
  columns to numeric (turning any unparseable value into a proper null), drops rows
  with no usable date, and removes physically impossible values such as negative
  precipitation.
- **Duplicates** are guarded at two levels: pandas drops duplicate (city, date) rows
  during cleaning, and the database enforces a `UNIQUE (city_id, weather_date)`
  constraint so re-running the load never creates duplicate rows.
- **Missing values** are stored as proper SQL `NULL`s rather than sentinel values, so
  aggregate functions like `AVG` ignore them correctly.
