import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os

CSV_FILENAME = "telemetry_log.csv"

def plot_telemetry():
    if not os.path.exists(CSV_FILENAME):
        print(f"[Error] {CSV_FILENAME} not found. Run main_pipeline.py first to log data.")
        return
        
    df = pd.read_csv(CSV_FILENAME)
    if df.empty or len(df) < 1:
        print("[Error] CSV log is empty or has insufficient data points.")
        return
        
    df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'])
    
    # Create figure with balanced margins
    fig, axes = plt.subplots(5, 1, figsize=(12, 13))
    ax_kp, ax_xray, ax_freq, ax_height, ax_nmf2 = axes
    
    fig.subplots_adjust(left=0.08, right=0.91, top=0.90, bottom=0.07, hspace=0.32)
    
    fig.suptitle(
        "Real-Time Space Weather & Ionosphere Dashboard\n"
        "(Click any data point on any line to inspect values)", 
        fontsize=13, fontweight='bold', y=0.95
    )
    
    line_metadata = {}

    for ax in axes:
        ax.tick_params(direction='out', which='both', length=5, width=1)
        ax.grid(True, linestyle='--', alpha=0.5)

    # ----------------------------------------------------
    # PANEL 1: Geomagnetic Drivers (Kp Index & IMF Bz)
    # ----------------------------------------------------
    line_kp = ax_kp.plot(
        df['timestamp_utc'], df['kp_index'], 
        label='Kp Index (Storm Level)', color='tab:red', linewidth=1.5, marker='o', markersize=3.5,
        picker=5
    )[0]
    line_metadata[line_kp] = {"name": "Kp Index (Storm Level)", "col": "kp_index", "unit": ""}
    
    ax_kp_twin = ax_kp.twinx()
    ax_kp_twin.tick_params(direction='out', length=5)
    line_bz = ax_kp_twin.plot(
        df['timestamp_utc'], df['imf_bz'], 
        label='IMF Bz (nT)', color='tab:blue', linestyle='--', linewidth=1.2, marker='s', markersize=3.5,
        picker=5
    )[0]
    line_metadata[line_bz] = {"name": "IMF Bz (Solar Magnetic Field)", "col": "imf_bz", "unit": "nT"}
    
    ax_kp.set_ylim(-0.5, 9.5)
    bz_min = df['imf_bz'].min() if not df['imf_bz'].isna().all() else -10.0
    bz_max = df['imf_bz'].max() if not df['imf_bz'].isna().all() else 10.0
    ax_kp_twin.set_ylim(min(bz_min - 2, -10.0), max(bz_max + 2, 10.0))
    ax_kp_twin.axhline(0, color='blue', linestyle=':', alpha=0.5, label='Neutral Line (0 nT)')
    
    ax_kp.set_ylabel("Kp Index", color='tab:red', fontweight='bold', fontsize=9)
    ax_kp_twin.set_ylabel("IMF Bz (nT)", color='tab:blue', fontweight='bold', fontsize=9, labelpad=12)
    
    lines_1, labels_1 = ax_kp.get_legend_handles_labels()
    lines_2, labels_2 = ax_kp_twin.get_legend_handles_labels()
    ax_kp.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', framealpha=0.85, fontsize=8)

    # ----------------------------------------------------
    # PANEL 2: Solar X-Ray Flux
    # ----------------------------------------------------
    line_xray = ax_xray.plot(
        df['timestamp_utc'], df['xray_flux'], 
        label='Solar X-Ray Flux', color='tab:orange', linewidth=1.5, marker='x', markersize=4,
        picker=5
    )[0]
    line_metadata[line_xray] = {"name": "Solar X-Ray Flux", "col": "xray_flux", "unit": "W/m²"}
    
    ax_xray.set_ylabel("X-Ray Flux (W/m²)", fontweight='bold', fontsize=9)
    ax_xray.set_yscale('log')
    ax_xray.legend(loc='upper right', framealpha=0.85, fontsize=8)

    # ----------------------------------------------------
    # PANEL 3: Radio Frequencies (foF2, MUF, foE)
    # ----------------------------------------------------
    line_fof2 = ax_freq.plot(
        df['timestamp_utc'], df['fof2_mhz'], 
        label='Critical Freq (foF2)', color='tab:purple', linewidth=1.5, marker='o', markersize=3.5,
        picker=5
    )[0]
    line_metadata[line_fof2] = {"name": "foF2 (F2 Reflection Limit)", "col": "fof2_mhz", "unit": "MHz"}
    
    line_muf = ax_freq.plot(
        df['timestamp_utc'], df['muf_mhz'], 
        label='Max Usable Freq (MUF)', color='tab:green', linestyle='-.', linewidth=1.5, marker='^', markersize=3.5,
        picker=5
    )[0]
    line_metadata[line_muf] = {"name": "MUF (Max Usable Frequency)", "col": "muf_mhz", "unit": "MHz"}
    
    line_foe = ax_freq.plot(
        df['timestamp_utc'], df['foe_mhz'], 
        label='E-Layer Freq (foE)', color='deepskyblue', linestyle=':', linewidth=1.8, marker='d', markersize=3.5,
        picker=5
    )[0]
    line_metadata[line_foe] = {"name": "foE (E-Layer Reflection Limit)", "col": "foe_mhz", "unit": "MHz"}
    
    ax_freq.set_ylabel("Frequency (MHz)", fontweight='bold', fontsize=9)
    ax_freq.legend(loc='upper right', framealpha=0.85, fontsize=8)

    # ----------------------------------------------------
    # PANEL 4: Peak Ionization Height (hmF2)
    # ----------------------------------------------------
    line_hmf2 = ax_height.plot(
        df['timestamp_utc'], df['hmf2_km'], 
        label='Peak Height (hmF2)', color='tab:brown', linewidth=1.5, marker='^', markersize=3.5,
        picker=5
    )[0]
    line_metadata[line_hmf2] = {"name": "hmF2 (Ionization Altitude)", "col": "hmf2_km", "unit": "km"}
    
    ax_height.set_ylabel("Height (km)", fontweight='bold', fontsize=9)
    ax_height.legend(loc='upper right', framealpha=0.85, fontsize=8)

    # ----------------------------------------------------
    # PANEL 5: Peak Electron Density (NmF2)
    # ----------------------------------------------------
    line_nmf2 = ax_nmf2.plot(
        df['timestamp_utc'], df['nmf2_m3'], 
        label='Electron Density (NmF2)', color='tab:cyan', linewidth=1.5, marker='d', markersize=3.5,
        picker=5
    )[0]
    line_metadata[line_nmf2] = {"name": "NmF2 (Electron Density)", "col": "nmf2_m3", "unit": "m⁻³"}
    
    ax_nmf2.set_ylabel("NmF2 (m⁻³)", fontweight='bold', fontsize=9)
    ax_nmf2.set_xlabel("UTC Timeline", fontweight='bold', fontsize=9)
    ax_nmf2.legend(loc='upper right', framealpha=0.85, fontsize=8)
    
    ax_nmf2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax_nmf2.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()

    # ----------------------------------------------------
    # SMART ANNOTATION BOX VIA NATIVE PICK EVENT
    # ----------------------------------------------------
    initial_annot = ax_nmf2.annotate(
        "", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.5", fc="aliceblue", alpha=0.95, ec="steelblue", lw=1.2),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color="steelblue")
    )
    initial_annot.set_visible(False)
    annot_holder = [initial_annot]

    def on_pick(event):
        try:
            clicked_line = event.artist
            if clicked_line in line_metadata:
                meta = line_metadata[clicked_line]
                best_idx = event.ind[0]
                
                row = df.iloc[best_idx]
                t_str = row['timestamp_utc'].strftime('%Y-%m-%d %H:%M UTC')
                val = row[meta['col']]
                
                if meta['col'] == 'xray_flux':
                    val_str = f"{val:.2e}"
                elif meta['col'] == 'nmf2_m3':
                    val_str = f"{val:.3e}"
                else:
                    val_str = f"{val}"
                    
                x_num = mdates.date2num(pd.to_datetime(row['timestamp_utc']))
                y_val = row[meta['col']]
                
                xlim = clicked_line.axes.get_xlim()
                x_fraction = (x_num - xlim[0]) / (xlim[1] - xlim[0]) if xlim[1] > xlim[0] else 0.5
                
                text_offset = (-180, 20) if x_fraction > 0.75 else (20, 20)
                
                annot_holder[0].remove()
                annot_holder[0] = clicked_line.axes.annotate(
                    f"Time: {t_str}\n{meta['name']}: {val_str} {meta['unit']}",
                    xy=(x_num, y_val), xytext=text_offset, textcoords="offset points",
                    bbox=dict(boxstyle="round,pad=0.5", fc="aliceblue", alpha=0.95, ec="steelblue", lw=1.2),
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color="steelblue")
                )
                annot_holder[0].set_visible(True)
                fig.canvas.draw_idle()
        except Exception as e:
            print(f"[Pick Error]: {e}")

    fig.canvas.mpl_connect('pick_event', on_pick)
    
    print("[Dashboard Ready] Click any data point on any line to explore the values.")
    plt.savefig('my_graph.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_telemetry()