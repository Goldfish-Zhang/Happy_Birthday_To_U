# Tidal Spiral — generative art from tidal data

This small project visualizes tidal time series as a moving spiral using
Pygame. The example uses synthetic tidal data but accepts a CSV at
`data/tides.csv` with columns `datetime,height`.

Run locally:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Controls:
- ESC: quit
- UP/DOWN: increase/decrease animation speed

If you are running headless (no display), I can modify the script to export
frames to disk instead of opening a Pygame window.
