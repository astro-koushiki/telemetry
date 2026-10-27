import math

def calculate_itu_metrics(drivers, station_coords):
    """
    Calculates ITU-R empirical ionospheric parameters with strict NaN handling.
    """
    metrics = {
        "fof2_mhz": float('nan'),
        "hmf2_km": float('nan'),
        "foe_mhz": float('nan'),
        "plasma_freq_mhz": float('nan'),
        "muf_mhz": float('nan'),
        "nmf2_m3": float('nan'),
        "r_scale": None
    }
    
    kp = drivers.get('kp_index', float('nan'))
    xray = drivers.get('xray_flux', float('nan'))
    
    # STRICT TELEMETRY CHECK: Abort if live drivers are missing
    if math.isnan(kp) or math.isnan(xray):
        return metrics
        
    try:
        base_fof2 = 5.5
        xray_boost = math.log10(max(xray, 1e-9)) + 9.0  
        kp_effect = 0.3 * kp  
        
        fof2 = base_fof2 + max(0.0, xray_boost * 0.4) + kp_effect
        fof2 = round(max(1.0, min(fof2, 25.0)), 2)
        
        # Explicit calculations for all parameters
        muf = round(fof2 * 3.0, 2)
        foe = round(2.5 + max(0.0, xray_boost * 0.15), 2)
        hmf2 = round(300.0 + (10.0 * kp), 1)
        nmf2_m3 = 1.24e10 * (fof2 ** 2)
        
        metrics["fof2_mhz"] = fof2
        metrics["hmf2_km"] = hmf2
        metrics["foe_mhz"] = foe
        metrics["plasma_freq_mhz"] = fof2
        metrics["muf_mhz"] = muf
        metrics["nmf2_m3"] = nmf2_m3
        
        if xray >= 1e-3: metrics["r_scale"] = "Extreme (R5)"
        elif xray >= 1e-4: metrics["r_scale"] = "Severe (R4)"
        elif xray >= 1e-5: metrics["r_scale"] = "Strong (R3)"
        elif xray >= 1e-6: metrics["r_scale"] = "Moderate (R2)"
        elif xray >= 1e-7: metrics["r_scale"] = "Minor (R1)"
        else: metrics["r_scale"] = "Normal (R0)"
        
    except Exception as e:
        print(f"[Warning] ITU model calculation error: {e}")
        
    return metrics