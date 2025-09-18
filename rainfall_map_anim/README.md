# Rainfall Map Animation

This small project generates synthetic monthly average rainfall for a set of
stations and animates the last 100 years as colored dots on a world map using
matplotlib.

Files:
- `rainfall_data.py`: generates `data/rainfall.csv` (synthetic data)
- `animate_rainfall.py`: reads the CSV and creates an animation (shows with plt.show() or saves mp4)
- `requirements.txt`: runtime dependencies. `cartopy` is optional but recommended for better maps.

Quick start (Windows PowerShell):

```powershell
python -m pip install -r requirements.txt
python rainfall_data.py
python animate_rainfall.py --years 100
```

To save an mp4 (requires ffmpeg on PATH):

```powershell
python animate_rainfall.py --save rainfall_anim.mp4 --fps 30 --years 100
```

Notes:
- The data is synthetic and intended as a demo. Replace `data/rainfall.csv` with real data in the same schema to use real observations.
- If `cartopy` isn't installed, the script plots lon/lat in a simple axes.

Trail effect:
- The animation supports a fading trail so previous months remain visible with lower opacity. Use `--trail-months` to control how many months are shown (default 24):

```powershell
python animate_rainfall.py --years 100 --trail-months 24
```

Lower `--trail-months` to shorten the trail for better performance or visual clarity.
