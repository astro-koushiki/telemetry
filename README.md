autonomous real time  ionosphere telemetry and wave propogation. 


An autonomous telemetry pipeline that adjoins live space weather observations, real-time WebSDR radio signal status, and ITU-R empirical physics modeling to study high-frequency (HF) radio wave propagation and ionospheric dynamics.

SCIENTIFIC INSPIRATION AND OVERVIEW:
 the radio waves bounce off the ionosphere , this happening is used to propogate radio waves over longer distances . however, the weather from the sun constantly changes the ionosphere's conditions. this model helps undertsand the changing ionospheric dynamics and skywave propogation.

THIS PROJECT : 
solves a alluring riddle about how well the mathematical calculations can harmonize with the real occuring in the sky .it does so By capturing continuous observational data without synthetic fallbacks, the pipeline evaluates the real-time residual error between mathematical model predictions and live radio propagation conditions.

FEATURES:

1. automaticallly fetching  the real time geomagnetic activity from noaa weather satellite. to calculate ionosphere's ability to bounce radio waves.
2. Live link monitoring against the University of Twente WebSDR station (`twente_nl_01`) in Enschede, Netherlands.
3. plot graphs to understand better about the waves which are required to connect the world .

>system architecture:
   ```text
   ┌─────────────────────────┐
   │  NOAA SWPC Live Feeds   │
   │  (Kp, X-Ray, IMF Bz)    │
   └────────────┬────────────┘
                │
                ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│ Twente WebSDR Telemetry ├──►│  ITU-R Physics Model    │
│    (Observational)      │   │  (itu_model.py)         │
└─────────────────────────┘   └────────────┬────────────┘
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
PROJECT STRUCTURE :


├── config.py              # NOAA endpoints, station metadata, and default parameters

├── noaa_fetcher.py        # Live SWPC space weather JSON API ingestion module

├── sdr_fetcher.py         # University of Twente WebSDR status fetcher

├── itu_model.py           # Empirical ITU-R physics calculation engine

├── main_pipeline.py       # live telemetry execution loop

├── plot_telemetry.py      # Multi-panel matplotlib data visualization 

├── telemetry_log.csv      # Real-time logged dataset

└── README.md              # Project documentation


>instllations and quick refernce guide:

1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

2. set up workspace :

'''Clone or enter project folder'''
bash 
cd /path/to/project/folder

'''Create virtual environment''' 
python3 -m venv env

''' Activate virtual environment'''
  source env/bin/activate

3. Install Dependencies

Bash
pip install requests pandas matplotlib

RUN THE CONDUIT:

1. run the teletry logger 

Bash
python -u main_pipeline.py

2. render live graphs :
python plot_telemetry.py

>YIELDED OUTCOMES:
The visualization script unfolds 4 sychronized graphs:
1. Real-time Kp index, X-Ray flux, and IMF Bz
2. Critical Frequency (foF2), Maximum Usable Frequency (MUF), and Optimum Working Frequency (FOT).
3. Real-part wave impedance  across the ionospheric medium.
4. Direct comparative tracking and residual error analysis .


