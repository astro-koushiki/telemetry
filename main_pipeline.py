import time
import csv
import json
import os
import math
from datetime import datetime
from config import STATION_COORDINATES, POLL_INTERVAL_SEC
from noaa_fetcher import fetch_space_weather
from itu_model import calculate_itu_metrics

CSV_FILENAME = "telemetry_log.csv"
JSON_FILENAME = "telemetry_log.json"

def init_logs():
    """Initializes both CSV and JSON log files if they don't exist."""
    if not os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp_utc", "kp_index", "xray_flux", "imf_bz", 
                "fof2_mhz", "foe_mhz", "hmf2_km", "plasma_freq_mhz", 
                "muf_mhz", "nmf2_m3", "r_scale"
            ])
            
    if not os.path.exists(JSON_FILENAME):
        with open(JSON_FILENAME, mode='w') as f:
            json.dump([], f)

def log_data_entry(entry_dict, data_row):
    """Appends telemetry data to both CSV and JSON log files."""
    with open(CSV_FILENAME, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data_row)
        
    try:
        with open(JSON_FILENAME, mode='r') as f:
            data_list = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data_list = []
        
    data_list.append(entry_dict)
    
    with open(JSON_FILENAME, mode='w') as f:
        json.dump(data_list, f, indent=4)

def run_pipeline():
    init_logs()
    print(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}] Starting Ionospheric Pipeline...")
    print(f"  Station Coordinates -> Lat: {STATION_COORDINATES['lat']}, Lon: {STATION_COORDINATES['lon']}")
    
    while True:
        try:
            drivers = fetch_space_weather()
            itu_metrics = calculate_itu_metrics(drivers, STATION_COORDINATES)
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            
            kp = drivers.get('kp_index', float('nan'))
            xray = drivers.get('xray_flux', float('nan'))
            bz = drivers.get('imf_bz', float('nan'))
            
            fof2 = itu_metrics.get('fof2_mhz', float('nan'))
            foe = itu_metrics.get('foe_mhz', float('nan'))
            hmf2 = itu_metrics.get('hmf2_km', float('nan'))
            plasma_freq = itu_metrics.get('plasma_freq_mhz', float('nan'))
            muf = itu_metrics.get('muf_mhz', float('nan'))
            nmf2 = itu_metrics.get('nmf2_m3', float('nan'))
            r_scale = itu_metrics.get('r_scale', 'Normal (R0)')
            
            entry_dict = {
                "timestamp_utc": timestamp,
                "kp_index": kp,
                "xray_flux": xray,
                "imf_bz": bz,
                "fof2_mhz": fof2,
                "foe_mhz": foe,
                "hmf2_km": hmf2,
                "plasma_freq_mhz": plasma_freq,
                "muf_mhz": muf,
                "nmf2_m3": nmf2,
                "r_scale": r_scale
            }
            
            data_row = [timestamp, kp, xray, bz, fof2, foe, hmf2, plasma_freq, muf, nmf2, r_scale]
            log_data_entry(entry_dict, data_row)
            
            print(f"\n[{timestamp}] Logged (Blackout Status: {r_scale}):")
            print(f"  Drivers  -> Kp: {kp} | X-Ray: {xray:.2e} | Bz: {bz} nT")
            print(f"  Physics  -> foF2: {fof2} MHz | foE: {foe} MHz | MUF: {muf} MHz | hmF2: {hmf2} km")
            
            time.sleep(POLL_INTERVAL_SEC)
            
        except KeyboardInterrupt:
            print("\nPipeline stopped by user.")
            break
        except Exception as e:
            print(f"[Error in pipeline loop]: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_pipeline()