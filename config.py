LOG_FILE = "telemetry_log.csv"
JSON_LOG_FILE = "telemetry_log.json"
POLL_INTERVAL_SEC = 10

# Your exact, locked station configuration schema
STATION_CONFIG = {
    "station_id": "twente_nl_01",
    "name": "University of Twente WebSDR",
    "lat": 52.24,
    "lon": 6.85,
    "base_url": "http://websdr.ewi.utwente.nl:8901"
}

# Standard ITU-R Physical & Model Constants
DEFAULT_SLAB_THICKNESS_KM = 400.0
DEFAULT_M3000F2_FACTOR = 3.0

# NOAA SPACE WEATHER API ENDPOINTS 
NOAA_CONFIG = {
    "kp_index_url": "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json",
    "xray_flux_url": "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json",
    
    "solar_wind_url": "https://services.swpc.noaa.gov/products/summary/solar-wind-mag-field.json"
}

