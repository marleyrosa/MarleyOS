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
    prev_speed = 0.0
    history = []

    while True:
        cycle_time = t % 20.0

        if cycle_time < 5.0:
            # EV_MODE
            progress = cycle_time / 5.0
            throttle = round(20.0 + 25.0 * math.sin(progress * math.pi), 1)
            brake = 0.0
            rpm_em = int(800 * progress + 600)
            rpm_ice = 0
            k0_press = 0.0
            k0_state = "OPEN"
            torque = round(throttle * 2.2, 1)
            mode = "EV_MODE"
            soc = max(10.0, soc - 0.015)
            temp_inv = max(40.0, temp_inv + 0.02)
            bsfc = 0.0
            gear = "1"
            active_clutch = "CLUTCH_1"

        elif cycle_time < 14.0:
            # P2_HYBRID_BOOST
            progress = (cycle_time - 5.0) / 9.0
            throttle = round(75.0 + 22.0 * math.sin(progress * math.pi), 1)
            brake = 0.0
            rpm_em = int(2000 + 3500 * progress)
            
            if progress < 0.22:
                rpm_ice = int(rpm_em * (progress / 0.22))
                k0_press = 2.0
                k0_state = "SYNC"
                bsfc = 330.0
                gear = "2"
                active_clutch = "CLUTCH_2"
            elif progress < 0.45:
                rpm_ice = int(rpm_em * 0.96)
                k0_press = 10.0
                k0_state = "SLIP"
                bsfc = 285.0
                gear = "3"
                active_clutch = "CLUTCH_1"
            elif progress < 0.72:
                rpm_ice = rpm_em
                k0_press = 18.0
                k0_state = "LOCKED"
                bsfc = 240.0
                gear = "4"
                active_clutch = "CLUTCH_2"
            else:
                rpm_ice = rpm_em
                k0_press = 18.0
                k0_state = "LOCKED"
                bsfc = 230.0
                gear = "5"
                active_clutch = "CLUTCH_1"

            torque = round(170.0 + 130.0 * progress, 1)
            mode = "P2_HYBRID_BOOST"
            soc = max(10.0, soc - 0.05)
            temp_inv = min(95.0, temp_inv + 0.12)

        else:
            # REGEN_BRAKE
            progress = (cycle_time - 14.0) / 6.0
            throttle = 0.0
            brake = round(70.0 * (1.0 - progress), 1)
            rpm_em = max(0, int(3600 * (1.0 - progress)))
            rpm_ice = 0
            k0_press = 0.0
            k0_state = "OPEN"
            torque = round(-80.0 * (1.0 - progress), 1)
            mode = "REGEN_BRAKE"
            soc = min(98.0, soc + 0.04)
            temp_inv = max(42.0, temp_inv - 0.06)
            bsfc = 0.0
            gear = "6"
            active_clutch = "CLUTCH_2"

        speed_kmh = round((rpm_em / 4.1) * (2 * math.pi * 0.315) * 0.06, 1)
        
        # Derivada inercial (Gx) em Gravidades (G)
        accel_mps2 = ((speed_kmh - prev_speed) / 3.6) / dt
        gx = round(accel_mps2 / 9.81, 2)
        gy = round(0.18 * math.sin(t * 0.8), 2) # Força lateral simulada em curva
        prev_speed = speed_kmh

        ev_range_km = round(((soc - 10.0) / 100.0) * pack_capacity_kwh / 0.16, 1)

        row = [
            f"{t:.1f}",
            str(speed_kmh),
            gear,
            active_clutch,
            str(rpm_em),
            str(rpm_ice),
            f"{throttle:.1f}",
            f"{brake:.1f}",
            f"{torque:.1f}",
            f"{gx:.2f}",
            f"{gy:.2f}",
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

        temp_path = CSV_PATH + ".tmp"
        with open(temp_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp_s", "speed_kmh", "gear", "active_clutch", "rpm_em", 
                "rpm_ice", "throttle_pct", "brake_pct", "torque_nm", "gx", "gy", 
                "k0_press_bar", "k0_state", "soc_pct", "ev_range_km", "bsfc_g_kwh", 
                "temp_inv_c", "modo_propulsao", "status_motor"
            ])
            writer.writerows(history)
        for attempt in range(20):
            try:
                os.replace(temp_path, CSV_PATH)
                break
            except PermissionError:
                time.sleep(0.05)

        t = round(t + dt, 1)
        time.sleep(dt)

if __name__ == "__main__":
    run_telemetry_loop()
