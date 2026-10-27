Autonomous Real-Time Ionosphere Telemetry and Wave Propagation

An autonomous telemetry pipeline that ingests live space weather observations from NOAA and applies empirical ITU-R physics modeling to study high-frequency (HF) radio wave propagation and ionospheric dynamics.

---

##  Scientific Inspiration & Overview

Radio waves bounce off the ionosphere, enabling long-distance skywave propagation. However, solar activity constantly alters the ionosphere's density and critical frequencies. 

This model captures live space weather data directly from NOAA feeds without synthetic fallbacks, feeding it into empirical physics equations to calculate real-time ionospheric responses, critical frequencies, and maximum usable frequencies.

---

##  Features

1. **NOAA SWPC Ingestion:** Automatically fetches real-time geomagnetic and solar activity from NOAA Space Weather Prediction Center feeds (`Kp index`, `X-Ray flux`, and `IMF Bz`).
2. **ITU-R Physics Engine:** Computes critical ionospheric parameters from live solar inputs, including:
   * Critical Frequencies (`foF2`, `foE`)
   * Layer Heights (`hmf2`)
   * Plasma Frequency & Electron Density (`NmF2`)
   * Maximum Usable Frequency (`MUF`)
   * Storm Scaling Factors (`R-scale`)
3. **Data Logging:** Persistently writes calculated telemetry into `telemetry_log.csv` for chronological tracking (`timestamp_utc`, `kp_index`, `xray_flux`, `imf_bz`, `fof2_mhz`, `foe_mhz`, `hmf2_km`, `plasma_freq_mhz`, `muf_mhz`, `nmf2_m3`, `r_scale`).
4. **Multi-Panel Visualization:** Generates synchronized matplotlib diagnostics tracking solar inputs, critical frequencies, and ionospheric response parameters.

---

##  System Architecture

```text
┌─────────────────────────┐
│  NOAA SWPC Live Feeds   │
│  (Kp, X-Ray, IMF Bz)    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  ITU-R Physics Model    │
│  (itu_model.py)         │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  telemetry_log.csv      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Multi-Panel Diagnostics │
│  (plot_telemetry.py)    │
└─────────────────────────┘


##  project structure

Plaintext
├── config.py              # NOAA endpoints, metadata, and default parameters
├── noaa_fetcher.py        # Live SWPC space weather JSON API ingestion module
├── itu_model.py           # Empirical ITU-R physics calculation 
├── main_pipeline.py       # Live telemetry execution loop
├── plot_telemetry.py      # Multi-panel matplotlib data visualization 
├── telemetry_log.csv      # Real-time logged dataset
└── README.md              # Project documentation

