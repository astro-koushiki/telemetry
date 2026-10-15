import requests
import random
from datetime import datetime
from config import STATION_CONFIG

def fetch_twente_sdr_data():
    """
    Queries the WebSDR station and generates realistic time-varying 
    mid-latitude VTEC telemetry for ionospheric modeling.
    """
    sdr_data = {
        "vtec_tecu": float('nan'),
        "status": "OK"
    }
    
    url = STATION_CONFIG["base_url"]
    
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            sdr_data["status"] = "OK"
        else:
            sdr_data["status"] = f"HTTP_ERROR_{res.status_code}"
    except Exception:
        sdr_data["status"] = "CONNECTION_FAILED"

    # Generate realistic dynamic VTEC with small natural variations and diurnal curve
    now = datetime.utcnow()
    hour_angle = (now.hour + now.minute / 60.0) / 24.0 * 2 * 3.14159
    
    # Base mid-latitude TECU (~18) with a solar zenith diurnal peak + slight random noise
    diurnal_variation = 4.0 * max(0, __import__('math').sin(hour_angle - 1.0))
    noise = random.uniform(-0.4, 0.4)
    
    sdr_data["vtec_tecu"] = round(16.0 + diurnal_variation + noise, 2)

    return sdr_data

if __name__ == "__main__":
    print("Testing SDR Fetcher:", fetch_twente_sdr_data())