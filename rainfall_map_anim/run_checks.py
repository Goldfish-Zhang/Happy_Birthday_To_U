"""Quick runtime checks for the rainfall_map_anim project."""
import os
import csv
import importlib

print('Python executable:', __import__('sys').executable)

print('matplotlib:', 'available' if importlib.util.find_spec('matplotlib') else 'MISSING')
print('cartopy:', 'available' if importlib.util.find_spec('cartopy') else 'MISSING (optional)')

data_path = os.path.join(os.path.dirname(__file__), 'data', 'rainfall.csv')
if os.path.exists(data_path):
    with open(data_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = sum(1 for _ in reader) - 1
    print(f"Found data file: {data_path} with {rows} data rows")
else:
    print('Data file not found:', data_path)

try:
    import animate_rainfall as a
    print('animate_rainfall import: OK')
except Exception as e:
    print('animate_rainfall import: FAILED', e)
