LOG_FILE = "telemetry_log.csv"
JSON_LOG_FILE = "telemetry_log.json"
POLL_INTERVAL_SEC = 300

#  locked station configuration schema
STATION_COORDINATES = {
 "lat": 52.24,
    "lon": 6.85,
    
}

# Standard ITU-R Physical & Model Constants
DEFAULT_SLAB_THICKNESS_KM = 400.0
DEFAULT_M3000F2_FACTOR = 3.0

# NOAA SPACE WEATHER API ENDPOINTS 
NOAA_CONFIG = {
    "kp_index_url": "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json",
    "xray_flux_url": "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json",
    "solar_wind_url": "https://services.swpc.noaa.gov/products/summary/solar-wind-mag-field.json",
    "glotec_url": "https://services.swpc.noaa.gov/products/glotec/geojson_2d_urt.json" 
}

# ITU-R Regional Physics Coefficients (Zero hardcoded numbers in model logic)
ITU_MODEL_PARAMS = {
    "base_slab_thickness_km": 350.0,
    "kp_slab_coeff": 12.0,
    "lat_slab_coeff": 20.0,
    "chapman_factor": 1.6,
    "plasma_freq_constant": 9.0,
    "base_hmf2_km": 300.0,
    "kp_hmf2_coeff": 5.0,
    "lat_hmf2_coeff": 10.0,
   
}