import json
import pandas as pd


CITIES = ["San Francisco", "Mesa", "Seattle"]


def load_file(city, type, is_forecast):
    """
    Load raw JSON file and flatten it into a table.

    city ==> city name
    type ==> "raw_historical_" or "raw_forecast_"
    is_forecast ==> True for forecast files --> they carry an extra field
 
    Returns a DataFrame: one row per day, with a city_name column added.
    """

    fname = "data/" + type + city.lower().replace(" ", "_") + ".json"

    with open(fname) as f:
        data = json.load(f)

    df = pd.DataFrame(data["daily"])

    df["city_name"] = city
    if is_forecast:
        df["retrieved_on"] = data["retrieved_on"]

    return df       # return the dataframe


# profile/explore the data 
def profile(df, label):
    """
    check for Null, type, ranges, duplicates
    """

    print("PROFILE: " + label + "\n")
    print("Rows and columns:", df.shape)
    
    print("\nNULL per column: ", df.isnull().sum())

    print("/nSummary: ", df.describe())

    duplicates = df.duplicated(subset=["city_name", "time"]).sum()
    print("\nDuplicate rows (city, date):", duplicates)
    


def clean(df):
    """
    fix all the changes that were found during profiling
    """
    before = len(df)

    df = df.drop_duplicates(subset=["city_name", "time"], keep="first")     # drop any duplicated that are found

    # convert all date related items into timestamps
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df["sunrise"] = pd.to_datetime(df["sunrise"], errors="coerce")
    df["sunset"] = pd.to_datetime(df["sunset"], errors="coerce")

    numeric_cols = [
        "temperature_2m_max", "temperature_2m_min",
        "apparent_temperature_max", "apparent_temperature_min",
        "precipitation_sum", "wind_speed_10m_max",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["time"])     # drop rows without a date

    df = df[~(df["precipitation_sum"] < 0)]


    after = len(df)

    print("Removed " + str(before - after) + " rows (before:" + str(before) + " | now: " + str(after) + ")")
    return df

def process(pre, is_forecast, cleaned_csv, label):
    """
    run for one data type(forecast or historical)
    load city file, stack, profile & clean, save to cleaned csv
    """

    frames = []
    for city_name in CITIES:
        frames.append(load_file(city_name, pre, is_forecast))

    combined = pd.concat(frames, ignore_index=True)

    profile(combined, label)
    cleaned = clean(combined)
    cleaned.to_csv(cleaned_csv, index=False)
    print("Saved the cleaned data to", cleaned_csv)


def main():
    process("raw_historical_", False, "data/cleaned_historical.csv", "HISTORICAL")
 
    process("raw_forecast_", True, "data/cleaned_forecast.csv", "FORECAST")
 
 
if __name__ == "__main__":
    main()
 
