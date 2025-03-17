# src/preprocess_data.py
import pandas as pd
import os

RAW_CSV_PATH = "data/raw/city_day.csv"
PROCESSED_PARQUET_PATH = "data/processed/city_day.parquet"

def main():
    """Reads raw CSV, cleans data, and saves as Parquet for faster loading."""
    
    if not os.path.exists(RAW_CSV_PATH):
        print(f"Error: Raw CSV file not found at {RAW_CSV_PATH}")
        return

    # Read CSV and ensure Datetime column is properly parsed
    df = pd.read_csv(RAW_CSV_PATH, parse_dates=["Datetime"], low_memory=False)

    # Drop rows with missing Datetime
    df.dropna(subset=["Datetime"], inplace=True)

    # Ensure processed data directory exists
    os.makedirs(os.path.dirname(PROCESSED_PARQUET_PATH), exist_ok=True)

    # Convert to Parquet for better performance
    df.to_parquet(PROCESSED_PARQUET_PATH, index=False)
    print(f"✅ Processed data saved to {PROCESSED_PARQUET_PATH}")

if __name__ == "__main__":
    main()
