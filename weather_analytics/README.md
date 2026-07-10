# Weather Analytics Pipeline

A data engineering pipeline that pulls daily weather data for multiple cities from the
Open-Meteo API, profiles and cleans it with pandas, loads it into a normalized
PostgreSQL database, and answers operational questions with SQL.

Cities analyzed: **San Francisco, Mesa, Seattle** (chosen for contrasting climates).
Historical range: **full 2025 calendar year**. A 7-day forecast is also pulled as a bonus.

## Pipeline

```
Extract  →  Profile & Clean  →  Load  →  Analyze
(requests)     (pandas)      (psycopg)    (SQL)
```

Each stage writes a durable artifact (raw JSON → cleaned CSV → database tables →
query results), so the pipeline is restartable rather than one fragile script.

## Tech Stack

- **Python** (`requests`) — API ingestion
- **pandas** — profiling and cleaning
- **PostgreSQL** + **psycopg** — normalized storage
- **SQL** — schema (DDL) and analytical queries
- **python-dotenv** — database credentials via environment variables
- **Git / GitHub** — version control

## Project Structure

```
weather_analytics/
├── historical_data.py     # Extract: 2025 daily data from the archive API
├── forecast_data.py       # Extract: 7-day forecast (bonus)
├── profile_clean.py       # Profile + clean raw JSON into cleaned CSVs
├── load.py                # Load cleaned CSVs into PostgreSQL
├── sql/
│   ├── schema.sql         # DDL: cities, weather, forecast tables
│   └── queries.sql        # 7 analytical queries
├── data/                  # raw JSON + cleaned CSVs (gitignored)
├── .env                   # DB credentials (gitignored — see setup)
├── README.md
└── SUMMARY.md             # Written summary deliverable
```

## Setup

**1. Create and activate a virtual environment:**
```
python3 -m venv venv
source venv/bin/activate
```

**2. Install dependencies:**
```
pip install requests pandas psycopg python-dotenv
```

**3. Create a `.env` file** in the project root with your PostgreSQL credentials:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=weather_db
DB_USER=postgres
DB_PASSWORD=your_password
```

**4. Create the database:**
```
psql -U postgres -h localhost -c "CREATE DATABASE weather_db;"
```

## Run Order

```
# 1. Extract raw data from the APIs
python historical_data.py
python forecast_data.py

# 2. Profile and clean into CSVs
python profile_clean.py

# 3. Build the schema (creates cities, weather, forecast tables)
psql -U postgres -h localhost -d weather_db -f sql/schema.sql

# 4. Load cleaned data into PostgreSQL
python load.py
```

Then run the analytical queries:
```
psql -U postgres -h localhost -d weather_db -f sql/queries.sql
```

## Database Schema

- **cities** — one row per city (name, latitude, longitude). Parent table.
- **weather** — one row per city per day (historical). Foreign key to `cities`;
  `UNIQUE (city_id, weather_date)`.
- **forecast** — bonus table of predicted values, keyed by
  `(city_id, record_date, retrieved_on)` since forecasts are revised over time.

## Analytical Queries

1. Highest recorded temperature per city
2. Hottest month of the year per city (correlated subquery)
3. Total monthly precipitation by city
4. Windiest week of the year (shown as a date range)
5. Average rainfall per city (on rainy days)
6. Frequency of extreme temperature days per city (heat > 95°F, freezing < 32°F)
7. Average daylight length per city (from sunrise/sunset)
