"""Simple tidal data generator and loader.

Generates a synthetic tidal height time series (hourly) for N days.
"""
import math
import csv
from datetime import datetime, timedelta


def generate_synthetic_tide(start: datetime, hours: int):
    # simple sum of two sine waves to mimic semi-diurnal + diurnal
    data = []
    for i in range(hours):
        t = i / 24.0
        # semi-diurnal (~12h) and diurnal (~24h)
        h = 1.2 * math.sin(2 * math.pi * t * 2) + 0.4 * math.sin(2 * math.pi * t)
        # slow seasonal drift
        h += 0.1 * math.sin(2 * math.pi * (i / (24*365)))
        data.append((start + timedelta(hours=i), h))
    return data


def save_csv(data, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['datetime', 'height'])
        for dt, h in data:
            writer.writerow([dt.isoformat(), f"{h:.4f}"])


if __name__ == '__main__':
    start = datetime.now()
    data = generate_synthetic_tide(start, hours=24*30)
    import os
    os.makedirs('data', exist_ok=True)
    save_csv(data, 'data/tides.csv')
    print('Saved synthetic tide data to data/tides.csv')
