import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.core.config import settings

def check_source() -> None:
    flights_path = os.path.join(settings.DATA_DIR, "flights_data.csv")
    
    print("=== SkyMind AI Data Diagnostics ===")
    print(f"Target Directory: {os.path.abspath(settings.DATA_DIR)}")
    
    if os.path.exists(flights_path):
        file_size = os.path.getsize(flights_path)
        with open(flights_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # If the file exists and has more lines than our tiny fallback, it's your real data!
        if len(lines) > 4:
            print(f" STATUS: SUCCESS! Using your custom dataset.")
            print(f" File Size: {file_size} bytes")
            print(f" Total Rows Found: {len(lines) - 1} entries")
        else:
            print(" STATUS: WARNING! File found, but it appears to match the fallback structure size.")
    else:
        print(" STATUS: CRITICAL! Data directory not detected. Initializing safety defaults.")

if __name__ == "__main__":
    check_source()