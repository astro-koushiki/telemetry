import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Use absolute path to ensure it looks in the exact same folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "telemetry_log.csv")

def plot_comprehensive_telemetry():
    print(f" Looking for telemetry log at: {CSV_PATH}")
    
    if not os.path.exists(CSV_PATH):
        print(f" Error: telemetry_log.csv NOT FOUND at {CSV_PATH}.")
        print(" Make sure your pipeline (main_pipeline.py) has run and successfully written log rows.")
        return

    try:
        df = pd.read_csv(CSV_PATH)
        print(f" Success! Loaded {len(df)} rows from CSV.")
    except Exception as e:
        print(f" Error reading CSV file: {e}")
        return

    if df.empty:
        print(" Warning: telemetry_log.csv is empty.")
        return

    print(f"Available columns in CSV: {list(df.columns)}")

    # Convert timestamps and numeric columns safely
    df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'], errors='coerce')
    numeric_cols = ['kp_index', 'xray_flux', 'imf_bz', 'vtec_tecu', 'foF2_mhz', 'impedance_real']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['timestamp_utc', 'vtec_tecu', 'foF2_mhz'])
    
    if df.empty:
        print(" Warning: Rows exist, but all numeric values evaluated to NaN after cleaning.")
        return

    print(f" Plotting {len(df)} valid data points...")

    # Compute derived propagation metrics
    M3000_FACTOR = 3.0
    df['muf_mhz'] = df['foF2_mhz'] * M3000_FACTOR
    df['fot_mhz'] = df['muf_mhz'] * 0.85
    df['freq_ratio'] = df['muf_mhz'] / df['foF2_mhz']
    df['model_vtec_equiv'] = df['foF2_mhz'] * 2.35
    df['residual'] = df['model_vtec_equiv'] - df['vtec_tecu']

    # Create Multi-Panel Figure
    fig, axes = plt.subplots(4, 1, figsize=(12, 14), sharex=True)

    # Panel 1: Space Weather Drivers
    ax1 = axes[0]
    ax1.plot(df['timestamp_utc'], df['kp_index'], label='Kp Index', color='tab:red', marker='x')
    ax1.set_ylabel('Kp Index', color='tab:red')
    ax1.grid(True, alpha=0.3)
    ax1_twin = ax1.twinx()
    ax1_twin.plot(df['timestamp_utc'], df['imf_bz'], label='IMF Bz (nT)', color='tab:purple', linestyle=':')
    ax1_twin.set_ylabel('IMF Bz [nT]', color='tab:purple')
    ax1.set_title('Solar & Space Weather Drivers (Kp, X-Ray, IMF Bz)')

    # Panel 2: Frequencies
    ax2 = axes[1]
    ax2.plot(df['timestamp_utc'], df['foF2_mhz'], label='Critical Freq (foF2)', color='tab:blue', linewidth=2)
    ax2.plot(df['timestamp_utc'], df['muf_mhz'], label='Max Usable Freq (MUF)', color='tab:orange', linestyle='--')
    ax2.plot(df['timestamp_utc'], df['fot_mhz'], label='Optimum Freq (FOT)', color='tab:green', linestyle='-.')
    ax2.set_ylabel('Frequency [MHz]')
    ax2.set_title('ITU-R Frequencies & Max-to-Critical Ratio')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper left')

    # Panel 3: Impedance
    ax3 = axes[2]
    ax3.plot(df['timestamp_utc'], df['impedance_real'], label='Plasma Impedance (Ω)', color='tab:brown', marker='o')
    ax3.set_ylabel('Impedance [Ω]')
    ax3.set_title('Effective Plasma Wave Impedance')
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc='upper left')

    # Panel 4: Real vs Model & Residuals
    ax4 = axes[3]
    ax4.plot(df['timestamp_utc'], df['vtec_tecu'], label='Truth: SDR VTEC', color='tab:blue', linewidth=2, marker='s')
    ax4.plot(df['timestamp_utc'], df['model_vtec_equiv'], label='ITU Model Estimate', color='tab:orange', linestyle='--', linewidth=2)
    ax4.set_ylabel('VTEC [TECU]')
    ax4.set_title('Real vs. Model Data & Weather Residuals')
    ax4.grid(True, alpha=0.3)
    ax4.legend(loc='upper left')

    ax4_twin = ax4.twinx()
    ax4_twin.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax4_twin.plot(df['timestamp_utc'], df['residual'], label='Residual (Model - Truth)', color='tab:red', linestyle=':', marker='x')
    ax4_twin.set_ylabel('Residual Error [TECU]', color='tab:red')

    axes[3].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()

    plt.tight_layout()
    print(" Rendering matplotlib window...")
    plt.show()

if __name__ == "__main__":
    plot_comprehensive_telemetry()