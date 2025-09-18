"""Animate monthly average rainfall as colored dots on a world map.

This script reads `data/rainfall.csv` and animates the last 100 years of data
evenly over time. Each frame corresponds to one month; by default it will show
100 years = 1200 frames. The animation scrolls through time showing stations
as colored dots where color maps to rainfall amount.

Optional: If `cartopy` is available, a nicer map projection is used. Otherwise
it falls back to a simple scatter on lon/lat axes.
"""
import argparse
import csv
import math
import os
from collections import defaultdict
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    CARTOPY = True
except Exception:
    CARTOPY = False


def read_rainfall_csv(path):
    # returns dict {(year, month): list of (lat, lon, rainfall)}
    data = defaultdict(list)
    stations_meta = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            sid = r['station_id']
            lat = float(r['lat'])
            lon = float(r['lon'])
            year = int(r['year'])
            month = int(r['month'])
            rainfall = float(r['rainfall_mm'])
            data[(year, month)].append((lat, lon, rainfall))
            stations_meta[sid] = (lat, lon)
    return data, stations_meta


def get_sorted_months(data_keys):
    months = sorted(data_keys)
    return months


def animate(path="data/rainfall.csv", years=100, fps=30, save=None, trail_months=24):
    data, stations = read_rainfall_csv(path)
    months = get_sorted_months(data.keys())
    if not months:
        raise RuntimeError("No data found in CSV")

    # Determine last months to show: last `years` years
    last_year, last_month = months[-1]
    start_year = last_year - years + 1
    # Build an ordered list of months to animate
    anim_months = [m for m in months if (m[0] >= start_year)]

    # Flatten station positions (we'll plot per frame from values in data)
    lats = []
    lons = []
    # choose global bounds
    for sid, (lat, lon) in stations.items():
        lats.append(lat)
        lons.append(lon)

    fig = plt.figure(figsize=(12, 6))
    if CARTOPY:
        ax = plt.axes(projection=ccrs.Robinson())
        ax.add_feature(cfeature.LAND.with_scale('110m'), facecolor='#f0efe6')
        ax.add_feature(cfeature.COASTLINE.with_scale('110m'))
        plot_kwargs = {'transform': ccrs.PlateCarree()}
    else:
        ax = plt.axes()
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('Monthly avg rainfall (mm)')
        plot_kwargs = {}

    # We'll use a scatter for the most recent month and plot faded older points by setting alpha
    scat = ax.scatter([], [], s=20, cmap='Blues', vmin=0, vmax=150)
    cbar = plt.colorbar(scat, ax=ax, orientation='vertical', fraction=0.03)
    cbar.set_label('Rainfall (mm)')

    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    def init():
        scat.set_offsets(np.empty((0, 2)))
        scat.set_array(np.array([]))
        time_text.set_text('')
        return scat, time_text

    def update(frame):
        # For each frame, collect up to `trail_months` previous months (including current)
        start_idx = max(0, frame - (trail_months - 1))
        frames_to_draw = list(range(start_idx, frame + 1))

        all_offsets = []
        all_colors = []
        all_vals = []
        n_draw = len(frames_to_draw)
        for idx_pos, idx in enumerate(frames_to_draw):
            year, month = anim_months[idx]
            pts = data.get((year, month), [])
            if not pts:
                continue
            arr = np.array([[lon, lat] for (lat, lon, r) in pts])
            vals = np.array([r for (lat, lon, r) in pts])
            # Compute alpha: older frames get lower alpha. recent frame alpha = 1.0
            # idx_pos runs from 0..n_draw-1; we want older ones smaller alpha
            alpha = np.linspace(0.1, 1.0, n_draw)[idx_pos]
            # Build RGBA colors based on the colormap mapping values
            cmap = matplotlib.cm.get_cmap('Blues')
            norm = matplotlib.colors.Normalize(vmin=0, vmax=150)
            base_colors = cmap(norm(vals))
            # apply alpha fade
            base_colors[:, 3] = base_colors[:, 3] * alpha

            all_offsets.append(arr)
            all_vals.append(vals)
            all_colors.append(base_colors)

        if all_offsets:
            offsets = np.vstack(all_offsets)
            colors = np.vstack(all_colors)
            scat.set_offsets(offsets)
            # scatter accepts an array for colors via `facecolors`
            scat.set_facecolors(colors)
            # keep scalar array for colorbar (set to current month's values where available)
            # we'll set the scalar array to the most recent month values for colorbar
            last_pts = data.get(anim_months[frame], [])
            if last_pts:
                last_vals = np.array([r for (lat, lon, r) in last_pts])
                scat.set_array(last_vals)
        else:
            scat.set_offsets(np.empty((0, 2)))
            scat.set_facecolors(np.empty((0, 4)))
            scat.set_array(np.array([]))

        cyear, cmonth = anim_months[frame]
        time_text.set_text(f"{cyear}-{cmonth:02d} ({frame+1}/{len(anim_months)})")
        return scat, time_text

    frames = len(anim_months)
    interval = 1000 / fps

    anim = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=interval)

    if save:
        # Try to save using ffmpeg if available
        anim.save(save, fps=fps, dpi=150)
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description='Animate rainfall on a map')
    parser.add_argument('--data', default='data/rainfall.csv')
    parser.add_argument('--years', type=int, default=100)
    parser.add_argument('--fps', type=int, default=30)
    parser.add_argument('--save', default=None, help='Filename to save animation (mp4)')
    parser.add_argument('--trail-months', type=int, default=24, help='How many months to show as a fading trail (default 24)')
    args = parser.parse_args()
    animate(path=args.data, years=args.years, fps=args.fps, save=args.save, trail_months=args.trail_months)


if __name__ == '__main__':
    main()
