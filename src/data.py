## data.py

import pandas as pd
import geopandas as gpd
from datetime import date

df = pd.read_csv('data/raw/city_day.csv', parse_dates=["Datetime"])
df["Datetime"] = pd.to_datetime(df["Datetime"])

pollutants = ['AQI', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2',
              'O3', 'Benzene', 'Toluene', 'Xylene']

india_map = gpd.read_file("data/map/ne_110m_admin_0_countries.shp")
india_map = india_map[india_map['ADMIN'] == "India"]

city_coords = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946}
}
city_df = pd.DataFrame([{"City": k, "Latitude": v["lat"],
                       "Longitude": v["lon"]} for k, v in city_coords.items()])
