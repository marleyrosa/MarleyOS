import csv
import os
import time
import math

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")

def run_telemetry_loop():
    t = 0.0
    dt = 0.1
    soc = 82.0
    temp_inv = 45.0
    pack_capacity_kwh = 14.8
    history = []

    while True:
        cycle_time = t % 18.0

        if cycle_time < 5.0:
            # EV_MODE: Marcha 1 ou 2 (K1 ativa)
            progress = cycle_time / 5.0
            throttle = round(15.0 + 15.0 * math.sin(progress * math.pi), 1)
            rpm_em = int(800 * progress + 400)
            rpm_ice = 0
            k0_press = 0.0
            k0_state = "OPEN"
            torque = round(throttle * 2.2, 1)
            mode = "EV_MODE"
            soc = max(10.0, soc - 0.015)
            temp_inv = max(40.0, temp_inv + 0.02)
            bsfc = 0.0
            gear = "G1"
            k_clutch_active = "K1"

        elif cycle_time < 12.0:
            # P2_HYBRID_BOOST: Aceleração alta, progressão G2 -> G3 -> G4 (K1 e K2 alternando)
            progress = (cycle_time - 5.0) / 7.0
            throttle = round(65.0 + 30.0 * math.sin(progress * math.pi), 1)
            rpm_em = int(1800 + 3200 * progress)
            
            if progress < 0.25:
                rpm_ice = int(rpm_em * (progress / 0.25))
                k0_press = 1.0
                k0_state = "SYNC"
                bsfc = 340.0
                gear = "G2"
                k_clutch_active = "K2"
            elif progress < 0.45:
                rpm_ice = int(rpm_em * 0.95)
                k0_press = round(3.0 + 12.0 * ((progress - 0.25) / 0.20), 1)
                k0_state = "SLIP"
                bsfc = 280.0
                gear = "G3"
                k_clutch_active = "K1"
            else:
                rpm_ice = rpm_em
                k0_press = 18.0
                k0_state = "LOCKED"
                bsfc = 235.0
                gear = "G4"
                k_clutch_active = "K2"

            torque = round(160.0 + 120.0 * progress, 1)
            mode = "P2_HYBRID_BOOST"
            soc = max(10.0, soc - 0.05)
            temp_inv = min(95.0, temp_inv + 0.12)

        else:
            # REGEN_BRAKE: Marcha alta/desaceleração, freio K3 ou K2 ativo
            progress = (cycle_time - 12.0) / 6.0
            throttle = 0.0
            rpm_em = max(0, int(3500 * (1.0 - progress)))
            rpm_ice = 0
            k0_press = 0.0
            k0_state = "OPEN"
            torque = round(-75.0 * (1.0 - progress), 1)
            mode = "REGEN_BRAKE"
            soc = min(98.0, soc + 0.04)
            temp_inv = max(42.0, temp_inv - 0.06)
            bsfc = 0.0
            gear = "G5"
            k_clutch_active = "K3"

        speed_kmh = round((rpm_em / 4.1) * (2 * math.pi * 0.315) * 0.06, 1)
        ev_range_km = round(((soc - 10.0) / 100.0) * pack_capacity_kwh / 0.16, 1)

        row = [
            f"{t:.1f}",
            str(speed_kmh),
            gear,
            k_clutch_active,
            str(rpm_em),
            str(rpm_ice),
            f"{torque:.1f}",
            f"{k0_press:.1f}",
            k0_state,
            f"{soc:.1f}",
            f"{ev_range_km:.1f}",
            f"{bsfc:.0f}",
            f"{temp_inv:.1f}",
            mode,
            "NOMINAL"
        ]

        history.append(row)
        if len(history) > 6:
            history.pop(0)

        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp_s", "speed_kmh", "gear", "k_clutch_active", "rpm_em", 
                "rpm_ice", "torque_nm", "k0_press_bar", "k0_state", "soc_pct", 
                "ev_range_km", "bsfc_g_kwh", "temp_inv_c", "modo_propulsao", "status_motor"
            ])
            writer.writerows(history)

        t = round(t + dt, 1)
        time.sleep(dt)

if __name__ == "__main__":
    run_telemetry_loop()
