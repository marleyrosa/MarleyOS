import csv
import os
import time
import math

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")

def run_telemetry_loop():
    print("[+] Telemetry Feeder ativo a 10 Hz. Pressione Ctrl+C para encerrar.")
    t = 0.0
    dt = 0.1
    history = []

    while True:
        cycle_time = t % 18.0  # Ciclo completo de 18 segundos

        if cycle_time < 5.0:
            # Fase 1: EV_MODE (Partida suave puramente eletrica)
            progress = cycle_time / 5.0
            throttle = round(15.0 + 15.0 * math.sin(progress * math.pi), 1)
            rpm = int(800 * progress + 400)
            torque = round(throttle * 2.2, 1)
            iq = round(torque / 0.48, 1)
            mode = "EV_MODE"

        elif cycle_time < 12.0:
            # Fase 2: P2_HYBRID_BOOST (Aceleracao total com acoplamento K0)
            progress = (cycle_time - 5.0) / 7.0
            throttle = round(65.0 + 30.0 * math.sin(progress * math.pi), 1)
            rpm = int(1800 + 3200 * progress)
            torque = round(160.0 + 120.0 * progress, 1)
            iq = round(torque * 0.75, 1)
            mode = "P2_HYBRID_BOOST"

        else:
            # Fase 3: REGEN_BRAKE (Frenagem regenerativa)
            progress = (cycle_time - 12.0) / 6.0
            throttle = 0.0
            rpm = max(0, int(3500 * (1.0 - progress)))
            torque = round(-75.0 * (1.0 - progress), 1)
            iq = round(torque / 0.48, 1)
            mode = "REGEN_BRAKE"

        row = [
            f"{t:.1f}",
            str(rpm),
            f"{torque:.1f}",
            f"{throttle:.1f}",
            f"{iq:.1f}",
            mode,
            "NOMINAL"
        ]

        history.append(row)
        if len(history) > 6:
            history.pop(0)

        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp_s", "rpm", "torque_nm", "throttle_pct", "iq_a", "modo_propulsao", "status_motor"])
            writer.writerows(history)

        t = round(t + dt, 1)
        time.sleep(dt)

if __name__ == "__main__":
    run_telemetry_loop()
