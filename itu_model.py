import math

def compute_ionospheric_physics(vtec_tecu, operating_freq_mhz=10.0, solar_kp=0.0):
    """
    Computes ionospheric parameters (foF2, hmF2, slab thickness, plasma frequency, impedance)
    using ITU-R standard approximations based on live VTEC and solar Kp index.
    """
    metrics = {
        "foF2_mhz": float('nan'),
        "hmF2_km": float('nan'),
        "slab_thickness_km": float('nan'),
        "plasma_freq_mhz": float('nan'),
        "impedance_real": float('nan')
    }
    
    try:
        if vtec_tecu is None or math.isnan(vtec_tecu) or vtec_tecu <= 0:
            return metrics
            
        # 1. Slab Thickness (km) increases slightly with geomagnetic activity (Kp)
        slab_thickness = 350.0 + (solar_kp * 12.0)
        metrics["slab_thickness_km"] = float(slab_thickness)
        
        # 2. Peak Electron Density NmF2 (electrons/m^3) derived from VTEC and slab thickness
        total_electrons_m2 = vtec_tecu * 1e16
        mean_density = total_electrons_m2 / (slab_thickness * 1000.0)
        nmf2 = mean_density * 1.6  # Chapman layer peak factor
        
        # 3. Critical Frequency foF2 (MHz) = 9.0 * sqrt(NmF2 / 10^12)
        fof2 = 9.0 * math.sqrt(max(0.0, nmf2 / 1e12))
        metrics["foF2_mhz"] = round(float(fof2), 2)
        
        # 4. Peak Height hmF2 (km) - standard mid-latitude baseline ~ 300 km
        hmf2 = 300.0 + (solar_kp * 5.0)
        metrics["hmF2_km"] = float(hmf2)
        
        # 5. Plasma Frequency (MHz) at F2 peak layer
        metrics["plasma_freq_mhz"] = round(float(fof2), 2)
        
        # 6. Effective RF Impedance (ohms) in ionospheric plasma medium
        freq = max(0.1, operating_freq_mhz)
        f_p = fof2
        if abs(freq - f_p) < 0.2:
            metrics["impedance_real"] = float('inf')  # Plasma cutoff / blackout
        else:
            permittivity = max(0.01, 1.0 - (f_p / freq)**2)
            impedance = 377.0 / math.sqrt(permittivity)
            metrics["impedance_real"] = round(float(impedance), 2)
            
    except Exception as e:
        print(f"[ITU Model Error] Computation failed: {e}")
        
    return metrics

if __name__ == "__main__":
    print("Testing ITU Model:", compute_ionospheric_physics(18.5, 10.0, 3.0))
