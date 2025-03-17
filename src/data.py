# src/data.py
import os
import pandas as pd
import geopandas as gpd

RAW_CSV_PATH = "data/raw/city_day.csv"
PROCESSED_PARQUET_PATH = "data/processed/city_day.parquet"
MAP_PATH = "data/map/ne_110m_admin_0_countries.shp"

# 1. Attempt to read Parquet
if os.path.exists(PROCESSED_PARQUET_PATH):
    df = pd.read_parquet(PROCESSED_PARQUET_PATH)
else:
    # Fallback: read CSV if no Parquet is found
    df_temp = pd.read_csv(RAW_CSV_PATH, parse_dates=["Datetime"])
    df_temp.to_parquet(PROCESSED_PARQUET_PATH, index=False)
    df = df_temp

# Pollutants list
pollutants = [
    'AQI', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx',
    'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene'
]

# Load shapefile, filter for India
india_map = gpd.read_file(MAP_PATH)
india_map = india_map[india_map['ADMIN'] == "India"]

# City coordinates (example)
city_coords = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946}
}

city_df = pd.DataFrame([
    {"City": c, "Latitude": coords["lat"], "Longitude": coords["lon"]}
    for c, coords in city_coords.items()
])
