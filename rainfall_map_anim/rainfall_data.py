"""Synthetic rainfall data generator.

Generates monthly average rainfall (mm) per station from 1925-01 to 2024-12
and writes to data/rainfall.csv with columns:
station_id,lat,lon,year,month,rainfall_mm
"""
import csv
import math
import os
import random
from datetime import datetime


def generate_stations(n=200, seed=42):
    random.seed(seed)
    stations = []
    for i in range(n):
        # Spread stations globally but focus on land latitudes
        lat = random.uniform(-60, 75)
        lon = random.uniform(-180, 180)
        stations.append((f"S{i:03d}", lat, lon))
    return stations


def monthly_rainfall_for_station(lat, lon, year, month, seed_base=0):
    # Base seasonal cycle: rainfall higher in summer hemisphere
    # Convert month to angle
    angle = (month - 1) / 12.0 * 2 * math.pi
    # Hemisphere seasonal: lat sign
    season_phase = 1 if lat >= 0 else -1
    seasonal = 50 + 40 * math.sin(angle * season_phase - 0.2)

    # Tropical boost
    tropical = 30 * math.exp(-abs(lat) / 20.0)

    # Long-term trend small random walk per station/year
    random.seed((int(lat * 1000) ^ int(lon * 1000) ^ year) + seed_base)
    noise = random.gauss(0, 10)

    value = seasonal + tropical + noise
    # Keep positive
    return max(0.0, value)


def generate_csv(path="data/rainfall.csv", start_year=1925, end_year=2024, stations=200):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    stations_list = generate_stations(n=stations)

    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["station_id", "lat", "lon", "year", "month", "rainfall_mm"])
        for sid, lat, lon in stations_list:
            for year in range(start_year, end_year + 1):
                for month in range(1, 13):
                    mm = monthly_rainfall_for_station(lat, lon, year, month)
                    writer.writerow([sid, f"{lat:.4f}", f"{lon:.4f}", year, month, f"{mm:.2f}"])


if __name__ == "__main__":
    print("Generating synthetic rainfall data to data/rainfall.csv...")
    generate_csv()
    print("Done.")
