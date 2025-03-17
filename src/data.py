# src/data.py
import os
import pandas as pd
import geopandas as gpd

RAW_CSV_PATH = "data/raw/city_day.csv"
PROCESSED_PARQUET_PATH = "data/processed/city_day.parquet"
MAP_PATH = "data/map/ne_110m_admin_0_countries.shp"

# Load data from Parquet if available (faster), otherwise from CSV
if os.path.exists(PROCESSED_PARQUET_PATH):
    df = pd.read_parquet(PROCESSED_PARQUET_PATH)
else:
    df = pd.read_csv(RAW_CSV_PATH, parse_dates=["Datetime"])
    os.makedirs(os.path.dirname(PROCESSED_PARQUET_PATH), exist_ok=True)  # Ensure folder exists
    df.to_parquet(PROCESSED_PARQUET_PATH, index=False)  # Convert to Parquet for future use

# Define pollutants list
pollutants = ['AQI', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']

# Load India map
if os.path.exists(MAP_PATH):
    india_map = gpd.read_file(MAP_PATH)
    india_map = india_map[india_map['ADMIN'] == "India"]
else:
    india_map = None  # Handle missing file gracefully

# Manually defining city coordinates
city_coords = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946}
}

city_df = pd.DataFrame([
    {"City": city, "Latitude": coords["lat"], "Longitude": coords["lon"]}
    for city, coords in city_coords.items()
])
