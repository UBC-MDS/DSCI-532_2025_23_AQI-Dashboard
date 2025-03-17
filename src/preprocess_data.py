# src/preprocess_data.py
import pandas as pd
import os

RAW_CSV_PATH = "data/raw/city_day.csv"
PROCESSED_PARQUET_PATH = "data/processed/city_day.parquet"

def main():
    """
    Reads the raw city_day.csv, performs cleaning/transformation,
    and saves it as a Parquet file in data/processed/.
    """
    df_temp = pd.read_csv(RAW_CSV_PATH, parse_dates=["Datetime"])
    
    # Example cleanup: drop rows if Datetime is missing
    df_temp.dropna(subset=["Datetime"], inplace=True)
    
    # Make sure 'data/processed' folder exists
    os.makedirs(os.path.dirname(PROCESSED_PARQUET_PATH), exist_ok=True)
    
    # Write out to Parquet
    df_temp.to_parquet(PROCESSED_PARQUET_PATH, index=False)
    print(f"Processed data saved to {PROCESSED_PARQUET_PATH}")

if __name__ == "__main__":
    main()
