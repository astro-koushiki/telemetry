import requests
import math
from config import NOAA_CONFIG

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def fetch_space_weather():
    space_weather_data = {
        "kp_index": float('nan'),
        "xray_flux": float('nan'),
        "imf_bz": float('nan'),
        "status": "partial"
    }

    # 1. Fetch Planetary K-index (Universal Handler for Lists & Dicts)
    try:
        response = requests.get(NOAA_CONFIG["kp_index_url"], headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            for row in reversed(data):
                try:
                    val = float('nan')
                    if isinstance(row, dict):
                        # If row is a dictionary, check all common Kp key variations
                        for k in ["kp", "Kp", "KP", "planetary_k", "estimated_kp"]:
                            if k in row and row[k] is not None:
                                val = float(row[k])
                                break
                    elif isinstance(row, list) and len(row) > 1:
                        # If row is a list, safely grab index 1 (ignoring header rows containing strings)
                        val = float(row[1])
                    
                    # If we successfully parsed a valid float, lock it in and exit loop
                    if not math.isnan(val):
                        space_weather_data["kp_index"] = val
                        break
                except (ValueError, TypeError, IndexError, KeyError):
                    continue
    except Exception as e:
        print(f"[Warning] Kp fetch failed ({type(e).__name__}): {e}")

    # 2. Fetch GOES X-Ray Flux
    try:
        response = requests.get(NOAA_CONFIG["xray_flux_url"], headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            channels = [row for row in data if row.get("energy") == "0.1-0.8nm"]
            if channels:
                space_weather_data["xray_flux"] = float(channels[-1]["flux"])
    except Exception as e:
        print(f"[Warning] X-ray flux fetch failed ({type(e).__name__}): {e}")

    # 3. Fetch Solar Wind IMF Bz (Universal Handler)
    try:
        response = requests.get(NOAA_CONFIG["solar_wind_url"], headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, dict):
            for key in ["bz_gsm", "Bz_gsm", "BZ_GSM", "bz", "Bz", "BZ"]:
                if key in data and data[key] is not None:
                    space_weather_data["imf_bz"] = float(data[key])
                    break
        elif isinstance(data, list) and len(data) > 0:
            for row in reversed(data):
                if isinstance(row, dict):
                    for key in ["bz_gsm", "Bz_gsm", "BZ_GSM", "bz", "Bz", "BZ"]:
                        if key in row and row[key] is not None:
                            space_weather_data["imf_bz"] = float(row[key])
                            break
                elif isinstance(row, list) and len(row) > 3:
                    try:
                        space_weather_data["imf_bz"] = float(row[3])
                        break
                    except (ValueError, TypeError, IndexError):
                        continue
                if not math.isnan(space_weather_data["imf_bz"]):
                    break
    except Exception as e:
        print(f"[Warning] Solar Wind Bz fetch failed ({type(e).__name__}): {e}")

    space_weather_data["status"] = "success"
    return space_weather_data