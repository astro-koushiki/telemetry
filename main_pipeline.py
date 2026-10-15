import time
import csv
import json
from datetime import datetime
from config import LOG_FILE, JSON_LOG_FILE, POLL_INTERVAL_SEC, STATION_CONFIG
from noaa_fetcher import fetch_space_weather
from sdr_fetcher import fetch_twente_sdr_data
from itu_model import compute_ionospheric_physics

def diagnose_ionospheric_state(record):
    
    impedance = record.get("impedance_real", 0)
    kp = record.get("kp_index", 0)
    
    print(f"--- [DIAGNOSTIC STATUS] ---")
    if impedance == float('inf') or str(impedance) == "inf":
        print(f" [EVENT] Plasma Cutoff / HF Radio Blackout Detected!")
    elif kp >= 5.0:
        print(f"⚡ [ACTIVITY] Geomagnetic Storm Condition Active (Kp = {kp}).")
    else:
        print(f" [NOMINAL] Pipeline active and tracking telemetry streams, delta=nan")
    
def run_pipeline():
    print(f"[{datetime.utcnow().isoformat()}] Starting Ionospheric Telemetry Pipeline...")
    
    while True:
        timestamp_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # 1. Fetch live data from NOAA and WebSDR modules
            noaa_data = fetch_space_weather()
            sdr_data = fetch_twente_sdr_data()
            
            vtec_val = sdr_data.get("vtec_tecu", float('nan'))
            kp_val = noaa_data.get("kp_index", float('nan'))
            xray_val = noaa_data.get("xray_flux", float('nan'))
            bz_val = noaa_data.get("imf_bz", float('nan'))
            
            # 2. Compute ionospheric physics metrics
            metrics = compute_ionospheric_physics(vtec_val, operating_freq_mhz=10.0, solar_kp=kp_val)
            
            # 3. Assemble complete telemetry record
            record = {
                "timestamp_utc": timestamp_utc,
                "station_id": STATION_CONFIG["station_id"],
                "station_name": STATION_CONFIG["name"],
                "lat": STATION_CONFIG["lat"],
                "lon": STATION_CONFIG["lon"],
                "base_url": STATION_CONFIG["base_url"],
                "kp_index": kp_val,
                "xray_flux": xray_val,
                "imf_bz": bz_val,
                "vtec_tecu": vtec_val,
                **metrics,
                "status": sdr_data.get("status", "OK")
            }
            
            # 4. Print EVERY telemetry parameter used in your graphs to the terminal

            print(f"  Station Target : {record['station_name']} ({record['station_id']})")
            print(f"  NOAA Space Wx  -> Kp Index: {kp_val} | X-Ray Flux: {xray_val} | IMF Bz: {bz_val} nT")
            print(f"  SDR Data       -> VTEC: {vtec_val} TECU")
            print(f"  ITU Model      -> Critical Freq (foF2): {metrics.get('foF2_mhz', float('nan'))} MHz")
            print(f"  Model Heights  -> Peak Height (hmF2): {metrics.get('hmF2_km', float('nan'))} km | Slab Thickness: {metrics.get('slab_thickness_km', float('nan'))} km")
            print(f"  RF & Impedance -> Plasma Frequency: {metrics.get('plasma_freq_mhz', float('nan'))} MHz | Impedance: {metrics.get('impedance_real', float('nan'))} ohms")
            print(f"  Stream Status  -> {record['status']}")
            
            diagnose_ionospheric_state(record)
            
            # 5. Save record to local CSV and JSON log files
            file_exists = False
            try:
                with open(LOG_FILE, "r") as f:
                    file_exists = True
            except FileNotFoundError:
                pass
                
            with open(LOG_FILE, mode="a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=record.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(record)
                
            with open(JSON_LOG_FILE, mode="a") as jf:
                jf.write(json.dumps(record) + "\n")

        except Exception as e:
            print(f"[{timestamp_utc}] [WARNING] Cycle failed: {e}")
            
        time.sleep(POLL_INTERVAL_SEC)

if __name__ == "__main__":
    run_pipeline()