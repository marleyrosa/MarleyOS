import http.server
import socketserver
import os
import csv
import json
import threading
import time
import subprocess
import uuid
import sys
import shutil
from urllib.parse import urlparse

MATLAB_BIN = shutil.which("matlab") or r"C:\Program Files\MATLAB\R2026a\bin\matlab.exe"

PORT = 8080
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
MCP_DIR = os.path.join(ROOT_DIR, "module_2_mcp")
if MCP_DIR not in sys.path:
    sys.path.insert(0, MCP_DIR)

from generate_default_dbc import generate_default_dbc
CSV_PATH = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")
SVG_PATH = os.path.join(ROOT_DIR, "module_1_rag", "knowledge_base", "p2_powertrain_topology.svg")
P2HEV_MODEL_PATH = os.path.join(ROOT_DIR, "Model", "P2HEVModel", "P2HybridVehicle.slx")
P2HEV_SIGNALS = [
    "VehicleSpeed", "HVBatSOC", "BusVoltage", "HVBatCurrent", "EngTrqReq",
    "EMTrqReq", "EngineOn", "TransmissionRatio", "EMSpeed", "BrakeTorque",
    "SpeedSetPoint",
]
MIL_RUN_STATE = {
    "run_id": None,
    "status": "idle",
    "message": "Nenhuma execucao MIL solicitada.",
    "result": None,
}
MIL_RUN_LOCK = threading.Lock()


def load_topology_svg():
    """Load topology SVG content to inline into the HTML page."""
    if os.path.exists(SVG_PATH):
        try:
            with open(SVG_PATH, "r", encoding="utf-8") as f:
                svg = f.read()
                if "<?xml" in svg:
                    svg = svg[svg.find("<svg"):]
                return svg
        except Exception:
            pass
    return '<div style="color:var(--text-muted); padding:20px; text-align:center;">SVG Topology not found</div>'


def open_simulink_model():
    """Launch MATLAB graphical desktop with the MIL_MarleyOS_Powertrain model loaded."""
    harness_dir = os.path.join(ROOT_DIR, "Model")
    model_dir = os.path.join(ROOT_DIR, "module_3_agents_simulink")
    mcp_dir = os.path.join(ROOT_DIR, "module_2_mcp")
    model_path = os.path.join(harness_dir, "MIL_MarleyOS_Powertrain.slx")
    
    # Method 1: ShellExecute via os.startfile (opens directly in user's physical Windows desktop)
    try:
        os.startfile(model_path)
        print(f"[SIMULINK] os.startfile executed successfully on {model_path}", flush=True)
        return True
    except Exception as e1:
        print(f"[SIMULINK] os.startfile failed: {e1}, attempting matlab -r...", flush=True)

    # Method 2: Fallback via matlab -r
    matlab_expr = (
        "addpath('%s'); addpath('%s'); addpath('%s'); "
        "open_system('MIL_MarleyOS_Powertrain');"
    ) % (
        harness_dir.replace("'", "''"),
        model_dir.replace("'", "''"),
        mcp_dir.replace("'", "''"),
    )
    try:
        p = subprocess.Popen(
            [MATLAB_BIN, "-r", matlab_expr],
            cwd=harness_dir,
        )
        print(f"[SIMULINK] Launched MATLAB GUI (PID {p.pid})", flush=True)
        return True
    except Exception as e2:
        print(f"[SIMULINK] Erro ao abrir Simulink: {e2}", flush=True)
        return False


def normalize_p2hev_row(row):
    """Map P2HEV Dataset export columns to the cockpit contract."""
    if "VehicleSpeed" not in row:
        return row
    return {
        "timestamp_s": row.get("timestamp_s", row.get("Time", "0")),
        "speed_kmh": row.get("VehicleSpeed", "0"),
        "gear": row.get("TransmissionRatio", "0"),
        "active_clutch": "CLUTCH_1" if float(row.get("EngineOn", 0) or 0) else "CLUTCH_2",
        "rpm_em": row.get("EMSpeed", "0"),
        "rpm_ice": "0",
        "throttle_pct": "0",
        "brake_pct": row.get("BrakeTorque", "0"),
        "torque_nm": row.get("EMTrqReq", "0"),
        "gx": "0",
        "gy": "0",
        "k0_press_bar": "0",
        "k0_state": "OPEN",
        "soc_pct": row.get("HVBatSOC", "0"),
        "ev_range_km": "0",
        "bsfc_g_kwh": "0",
        "temp_inv_c": "45.0",
        "modo_propulsao": "EV_MODE",
        "status_motor": "NOMINAL",
        "bus_voltage_v": row.get("BusVoltage", "0"),
        "battery_current_a": row.get("HVBatCurrent", "0"),
        "engine_torque_request_nm": row.get("EngTrqReq", "0"),
        "speed_setpoint_kmh": row.get("SpeedSetPoint", "0"),
    }


def enrich_telemetry_row(row):
    """Enrich raw CAN row with physical P2 MBD channels (Torque Split, FOC Iq, Delta RPM, etc)."""
    row = normalize_p2hev_row(row)
    try:
        rpm_em = float(row.get("rpm_em", 0) or 0)
        rpm_ice = float(row.get("rpm_ice", 0) or 0)
        torque = float(row.get("torque_nm", 0) or 0)
        mode = row.get("modo_propulsao", "EV_MODE")
        gear_str = str(row.get("gear", "1"))
        gear = int(gear_str) if gear_str.isdigit() else 1
        soc = float(row.get("soc_pct", 50) or 50)
        bsfc = float(row.get("bsfc_g_kwh", 0) or 0)

        delta_rpm = abs(rpm_ice - rpm_em)

        # Torque Split & FOC Iq (Kt = 0.48 Nm/A, PMSM pole pairs = 4)
        if mode == "EV_MODE":
            t_em = torque
            t_ice = 0.0
        elif mode == "P2_HYBRID_BOOST":
            if rpm_ice > 400:
                t_ice = min(170.0, max(0.0, torque * 0.58))
                t_em = torque - t_ice
            else:
                t_ice = 0.0
                t_em = torque
        elif mode == "REGEN_BRAKE":
            t_em = torque
            t_ice = 0.0
        else:
            t_ice = max(0.0, torque * 0.5)
            t_em = torque - t_ice

        iq_a = round(t_em / 0.48, 1)

        # Mechanical & Electrical Power (kW = T * RPM / 9549)
        p_em_kw = round((t_em * rpm_em) / 9549.0, 1) if rpm_em > 0 else 0.0
        p_ice_kw = round((t_ice * rpm_ice) / 9549.0, 1) if rpm_ice > 0 else 0.0
        p_total_kw = round(p_em_kw + p_ice_kw, 1)
        p_total_cv = round(p_total_kw * 1.35962, 1)

        # K0 3-Phase Hydraulics & Coupling state
        if delta_rpm > 150:
            k0_phase = "FASE 1: SYNC / OPEN"
            k0_phase_num = 1
        elif delta_rpm > 20:
            k0_phase = "FASE 2: SLIPPING"
            k0_phase_num = 2
        else:
            k0_phase = "FASE 3: LOCKED / COUPLED"
            k0_phase_num = 3

        # e-DCT Dual Shaft Next Gear Pre-selection
        if gear % 2 == 1:
            preselected_gear = str(min(6, gear + 1))
            preselected_clutch = "C2"
        else:
            preselected_gear = str(min(5, gear + 1)) if mode != "REGEN_BRAKE" else str(max(1, gear - 1))
            preselected_clutch = "C1"

        # BSFC Efficiency Zone (ICE Miller Cycle)
        if bsfc == 0 or rpm_ice < 400:
            bsfc_zone = "OFF (EV)"
            bsfc_pct = 0
        elif 225 <= bsfc <= 255:
            bsfc_zone = "SWEET SPOT (41% Efic.)"
            bsfc_pct = 95
        elif bsfc < 290:
            bsfc_zone = "CRUISE (36% Efic.)"
            bsfc_pct = 75
        else:
            bsfc_zone = "CARGA ELEVADA"
            bsfc_pct = 50

        # Electrical frequency (p = 4)
        elec_freq_hz = round((4.0 * rpm_em) / 60.0, 1)

        # High Voltage Bus (Nominal 350V)
        bus_voltage_v = round(340.0 + (soc / 100.0) * 20.0, 1)
        battery_current_a = round((p_em_kw * 1000.0) / bus_voltage_v, 1) if bus_voltage_v > 0 else 0.0

        row.update({
            "delta_rpm": round(delta_rpm, 0),
            "t_ice": round(t_ice, 1),
            "t_em": round(t_em, 1),
            "iq_a": iq_a,
            "p_em_kw": p_em_kw,
            "p_ice_kw": p_ice_kw,
            "p_total_kw": p_total_kw,
            "p_total_cv": p_total_cv,
            "k0_phase": k0_phase,
            "k0_phase_num": k0_phase_num,
            "preselected_gear": preselected_gear,
            "preselected_clutch": preselected_clutch,
            "bsfc_zone": bsfc_zone,
            "bsfc_pct": bsfc_pct,
            "elec_freq_hz": elec_freq_hz,
            "bus_voltage_v": bus_voltage_v,
            "battery_current_a": battery_current_a,
        })
    except Exception:
        pass
    return row


def read_telemetry_rows():
    rows = []
    for _ in range(5):
        if not os.path.exists(CSV_PATH):
            break
        try:
            with open(CSV_PATH, "r", encoding="utf-8") as telemetry_file:
                raw_rows = list(csv.DictReader(telemetry_file))
            rows = [enrich_telemetry_row(row) for row in raw_rows]
            break
        except (OSError, UnicodeDecodeError, ValueError):
            time.sleep(0.01)
    return rows


def get_html_page():
    svg_content = load_topology_svg()
    template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexusMBD | AI-Native Powertrain Engineering Suite</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --carbon-bg: #07090e;
            --panel-bg: rgba(14, 19, 29, 0.9);
            --panel-border: rgba(0, 229, 255, 0.18);
            --cyan: #00e5ff;
            --cyan-glow: rgba(0, 229, 255, 0.35);
            --green: #00e676;
            --green-glow: rgba(0, 230, 118, 0.35);
            --amber: #ff9100;
            --amber-glow: rgba(255, 145, 0, 0.35);
            --red: #ff1744;
            --purple: #b388ff;
            --text-primary: #f0f6fc;
            --text-muted: #8b949e;
            --font-mono: 'Orbitron', 'SF Mono', monospace;
            --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: var(--font-sans);
            background: radial-gradient(circle at 50% 10%, #111726 0%, var(--carbon-bg) 80%);
            color: var(--text-primary);
            padding: 8px 12px;
            min-height: 100vh;
        }

        /* HEADER BRAND */
        .brand-header {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 6px; padding: 2px 4px;
        }
        .brand-title {
            font-family: var(--font-mono); font-weight: 900; font-size: 1.15rem;
            letter-spacing: 1px; color: var(--cyan); text-shadow: 0 0 10px var(--cyan-glow);
        }
        .brand-sub {
            font-size: 0.65rem; color: var(--text-muted); font-family: var(--font-mono);
            letter-spacing: 0.5px;
        }

        /* TOP 4 SYMMETRICAL AUTOMOTIVE BLOCKS */
        .top-nav-grid {
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 8px;
        }
        .nav-card {
            height: 48px; background: var(--panel-bg); border: 1px solid var(--panel-border);
            border-radius: 6px; padding: 0 12px; display: flex; align-items: center; gap: 10px;
            text-decoration: none; color: inherit; transition: all 0.2s ease; position: relative;
            overflow: hidden; box-shadow: inset 0 1px 0 rgba(255,255,255,0.05); user-select: none;
        }
        .nav-card::before {
            content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%;
            background: var(--card-color, var(--cyan));
        }
        .nav-card:hover {
            border-color: var(--card-color, var(--cyan));
            box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
        }
        .nav-btn { cursor: pointer; }
        .nav-btn:active { transform: translateY(1px); }
        .nav-btn:disabled { opacity: 0.65; cursor: wait; }
        .nav-icon {
            width: 22px; height: 22px; stroke: var(--card-color, var(--cyan));
            stroke-width: 1.8; fill: none; flex-shrink: 0;
        }
        .nav-text-col { display: flex; flex-direction: column; justify-content: center; min-width: 0; }
        .nav-label { font-size: 0.58rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase; }
        .nav-title {
            font-family: var(--font-mono); font-size: 0.72rem; font-weight: 800;
            color: var(--card-color, var(--text-primary)); white-space: nowrap; overflow: hidden;
            text-overflow: ellipsis;
        }
        .pulse-dot {
            width: 7px; height: 7px; border-radius: 50%; background: var(--green);
            box-shadow: 0 0 8px var(--green); animation: pulse 1.2s infinite; flex-shrink: 0;
        }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

        /* SHIFT LIGHTS & GEAR CLUSTER */
        .shift-strip-container {
            background: var(--panel-bg); border: 1px solid var(--panel-border);
            border-radius: 6px; padding: 4px 10px; margin-bottom: 8px;
            display: flex; align-items: center; justify-content: space-between; gap: 10px;
        }
        .shift-lights { display: flex; gap: 4px; flex: 1; justify-content: center; align-items: center; }
        .led {
            width: 14px; height: 14px; border-radius: 2px; background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1); transition: all 0.08s ease;
        }
        .led.green.on { background: var(--green); border-color: #fff; box-shadow: 0 0 10px var(--green); }
        .led.yellow.on { background: var(--amber); border-color: #fff; box-shadow: 0 0 10px var(--amber); }
        .led.red.on { background: var(--red); border-color: #fff; box-shadow: 0 0 12px var(--red); }
        .led.blue.on { background: #00b0ff; border-color: #fff; box-shadow: 0 0 14px #00b0ff; animation: flash 0.15s infinite; }
        @keyframes flash { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }

        .gear-indicator-box {
            display: flex; align-items: center; gap: 8px; border-left: 2px solid rgba(255,255,255,0.1);
            padding-left: 10px;
        }
        .gear-current {
            font-family: var(--font-mono); font-size: 1.7rem; font-weight: 900;
            color: var(--cyan); text-shadow: 0 0 10px var(--cyan-glow); min-width: 24px; text-align: center;
        }
        .gear-details { display: flex; flex-direction: column; gap: 2px; font-size: 0.6rem; font-family: var(--font-mono); }
        .clutch-badge {
            background: rgba(255, 23, 68, 0.2); color: var(--red); border: 1px solid var(--red);
            border-radius: 3px; padding: 1px 4px; font-weight: bold; text-align: center;
        }
        .clutch-badge.c2 { background: rgba(0, 230, 118, 0.2); color: var(--green); border-color: var(--green); }

        /* MIL PROGRESS & FEEDBACK BANNER */
        .mil-feedback-banner {
            display: none; background: rgba(14, 19, 29, 0.95); border: 1px solid var(--cyan);
            border-radius: 6px; padding: 8px 12px; margin-bottom: 8px;
            font-family: var(--font-mono); font-size: 0.7rem; flex-direction: column; gap: 6px;
        }
        .mil-feedback-banner.visible { display: flex; }
        .mil-banner-row {
            display: flex; justify-content: space-between; align-items: center; width: 100%;
        }
        .mil-progress-track {
            width: 100%; height: 8px; background: rgba(0,0,0,0.5);
            border-radius: 4px; overflow: hidden; border: 1px solid rgba(0, 229, 255, 0.2);
            position: relative;
        }
        .mil-progress-bar {
            height: 100%; width: 0%;
            background: linear-gradient(90deg, var(--cyan), var(--green));
            box-shadow: 0 0 10px var(--cyan);
            transition: width 0.3s ease;
            background-size: 20px 20px;
            background-image: linear-gradient(
                45deg, rgba(255, 255, 255, 0.2) 25%, transparent 25%,
                transparent 50%, rgba(255, 255, 255, 0.2) 50%, rgba(255, 255, 255, 0.2) 75%,
                transparent 75%, transparent
            );
            animation: progress-stripes 1s linear infinite;
        }
        @keyframes progress-stripes {
            0% { background-position: 0 0; }
            100% { background-position: 20px 0; }
        }

        /* PRIMARY GAUGES ROW */
        .metrics-grid-top {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(125px, 1fr));
            gap: 8px; margin-bottom: 8px;
        }
        .gauge-card {
            background: var(--panel-bg); border: 1px solid var(--panel-border);
            border-radius: 6px; padding: 6px 9px; position: relative; overflow: hidden;
            display: flex; flex-direction: column; justify-content: space-between;
        }
        .gauge-card::before {
            content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%;
            background: var(--card-accent, var(--cyan));
        }
        .gauge-card-title {
            font-size: 0.6rem; font-weight: 700; color: var(--text-muted);
            text-transform: uppercase; letter-spacing: 0.5px;
        }
        .gauge-card-val {
            font-family: var(--font-mono); font-size: 1.25rem; font-weight: 900;
            margin: 2px 0; display: flex; align-items: baseline; gap: 4px;
        }
        .gauge-card-unit { font-size: 0.62rem; color: var(--text-muted); font-weight: 600; }
        .gauge-sub-row {
            display: flex; justify-content: space-between; font-size: 0.6rem;
            color: var(--text-muted); font-family: var(--font-mono);
        }

        /* DYNAMIC ARCHITECTURE TOPOLOGY SVG SECTION */
        .topology-card {
            background: var(--panel-bg); border: 1px solid var(--panel-border);
            border-radius: 6px; padding: 8px 10px; margin-bottom: 8px;
        }
        .topology-header {
            display: flex; justify-content: space-between; align-items: center;
            font-size: 0.68rem; font-weight: 800; font-family: var(--font-mono);
            color: var(--cyan); margin-bottom: 6px; border-bottom: 1px solid rgba(255,255,255,0.06);
            padding-bottom: 4px;
        }
        .topology-status-badge {
            font-size: 0.62rem; font-weight: 700; font-family: var(--font-mono);
            background: rgba(0,0,0,0.4); border: 1px solid var(--cyan); border-radius: 4px;
            padding: 2px 8px; color: var(--cyan); transition: border-color 0.2s;
        }
        .topology-container {
            width: 100%; height: 165px; display: flex; justify-content: center;
            align-items: center; overflow: hidden; background: #070a10; border-radius: 4px;
        }
        .topology-container svg { width: 100%; height: 100%; max-height: 165px; }

        /* P2 MBD POWERTRAIN DETAILS */
        .p2-dashboard-grid {
            display: grid; grid-template-columns: 1.2fr 1.3fr 1.1fr;
            gap: 8px; margin-bottom: 8px;
        }
        .domain-box {
            background: var(--panel-bg); border: 1px solid var(--panel-border);
            border-radius: 6px; padding: 8px 10px; display: flex; flex-direction: column; gap: 6px;
        }
        .domain-title {
            font-family: var(--font-mono); font-size: 0.68rem; font-weight: 800;
            color: var(--cyan); text-transform: uppercase; display: flex;
            justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08);
            padding-bottom: 3px;
        }

        /* TORQUE SPLIT VISUALIZER */
        .torque-split-bar {
            width: 100%; height: 16px; background: rgba(0,0,0,0.5);
            border-radius: 3px; overflow: hidden; display: flex; border: 1px solid rgba(255,255,255,0.1);
        }
        .split-thermal {
            height: 100%; background: linear-gradient(90deg, #ff9100, #ff3d00);
            width: 50%; transition: width 0.15s ease;
        }
        .split-electric {
            height: 100%; background: linear-gradient(90deg, #00e5ff, #00e676);
            width: 50%; transition: width 0.15s ease;
        }
        .split-legend {
            display: flex; justify-content: space-between; font-size: 0.62rem;
            font-family: var(--font-mono); font-weight: 700;
        }

        /* MODE HERO BADGE */
        .mode-hero-badge {
            font-family: var(--font-mono); font-size: 0.78rem; font-weight: 900;
            text-align: center; padding: 4px; border-radius: 4px; letter-spacing: 0.5px;
        }
        .mode-hero-badge.EV_MODE {
            background: rgba(0, 230, 118, 0.15); color: var(--green); border: 1px solid var(--green);
            box-shadow: 0 0 10px var(--green-glow);
        }
        .mode-hero-badge.P2_HYBRID_BOOST {
            background: rgba(0, 229, 255, 0.18); color: var(--cyan); border: 1px solid var(--cyan);
            box-shadow: 0 0 12px var(--cyan-glow);
        }
        .mode-hero-badge.REGEN_BRAKE {
            background: rgba(255, 145, 0, 0.18); color: var(--amber); border: 1px solid var(--amber);
            box-shadow: 0 0 10px var(--amber-glow);
        }

        /* COMPACT RACING PEDALS (REDUCED BY HALF) */
        .pedals-compact-row {
            display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 2px;
        }
        .pedal-item {
            background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.06);
            border-radius: 4px; padding: 4px 6px; display: flex; align-items: center; gap: 8px;
        }
        .pedal-billet {
            width: 22px; height: 28px; border-radius: 3px; flex-shrink: 0;
            background: linear-gradient(145deg, #2b3548, #18202c);
            border: 1.5px solid #718096; position: relative;
            display: flex; flex-direction: column; justify-content: space-evenly; align-items: center;
        }
        .pedal-billet.throttle { border-color: var(--green); }
        .pedal-billet.brake { border-color: var(--red); }
        .billet-hole { width: 10px; height: 2px; background: #090c14; border-radius: 1px; }
        .pedal-info { display: flex; flex-direction: column; width: 100%; gap: 2px; }
        .pedal-title-bar {
            display: flex; justify-content: space-between; font-size: 0.58rem;
            font-family: var(--font-mono); font-weight: 700;
        }
        .pedal-mini-gauge {
            width: 100%; height: 5px; background: rgba(255,255,255,0.08);
            border-radius: 2px; overflow: hidden;
        }
        .pedal-mini-fill { height: 100%; width: 0%; transition: width 0.1s ease; }

        /* K0 COUPLING & DELTA RPM */
        .k0-coupling-meter {
            display: flex; flex-direction: column; gap: 3px; background: rgba(0,0,0,0.3);
            padding: 5px 7px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.06);
        }
        .k0-status-badge {
            font-family: var(--font-mono); font-size: 0.68rem; font-weight: 800;
            padding: 2px 4px; border-radius: 3px; text-align: center;
        }
        .k0-status-badge.LOCKED { background: rgba(0,230,118,0.2); color: var(--green); border: 1px solid var(--green); }
        .k0-status-badge.SLIP { background: rgba(0,229,255,0.2); color: var(--cyan); border: 1px solid var(--cyan); }
        .k0-status-badge.SYNC { background: rgba(255,145,0,0.2); color: var(--amber); border: 1px solid var(--amber); }
        .k0-status-badge.OPEN { background: rgba(255,255,255,0.1); color: var(--text-muted); border: 1px solid rgba(255,255,255,0.2); }

        .meter-bar-track {
            width: 100%; height: 6px; background: rgba(255,255,255,0.07);
            border-radius: 3px; overflow: hidden;
        }
        .meter-bar-fill { height: 100%; transition: width 0.15s ease; }

        /* DUAL-SHAFT DCT MATRIX */
        .dct-matrix {
            display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-family: var(--font-mono);
            font-size: 0.62rem; background: rgba(0,0,0,0.25); padding: 5px; border-radius: 4px;
        }
        .shaft-col { display: flex; flex-direction: column; gap: 3px; }
        .shaft-title { color: var(--text-muted); font-size: 0.58rem; font-weight: 800; }
        .gear-nodes { display: flex; gap: 3px; }
        .gear-node {
            width: 18px; height: 18px; display: flex; justify-content: center; align-items: center;
            border-radius: 3px; border: 1px solid rgba(255,255,255,0.15); font-weight: 800;
        }
        .gear-node.active { background: var(--cyan); color: #000; border-color: #fff; box-shadow: 0 0 8px var(--cyan); }
        .gear-node.preselect { background: rgba(255, 145, 0, 0.3); color: var(--amber); border-color: var(--amber); }

        /* G-BOWL */
        .g-bowl-circle {
            width: 54px; height: 54px; border-radius: 50%; border: 1.5px solid rgba(0, 229, 255, 0.4);
            position: relative; background: radial-gradient(circle, rgba(0,229,255,0.05) 0%, rgba(0,0,0,0.8) 100%);
            display: flex; justify-content: center; align-items: center; margin: 0 auto;
        }
        .g-cross-h { position: absolute; width: 100%; height: 1px; background: rgba(255,255,255,0.12); }
        .g-cross-v { position: absolute; height: 100%; width: 1px; background: rgba(255,255,255,0.12); }
        .g-dot {
            width: 8px; height: 8px; border-radius: 50%; background: var(--cyan);
            position: absolute; transform: translate(0px, 0px); box-shadow: 0 0 8px var(--cyan);
            transition: transform 0.12s ease-out;
        }

        /* OSCILLOSCOPE INTERACTIVE CANVAS */
        .oscilloscope-section {
            background: var(--panel-bg); border: 1px solid var(--panel-border);
            border-radius: 6px; padding: 7px 10px; margin-bottom: 8px;
        }
        .scope-header {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 5px; flex-wrap: wrap; gap: 6px;
        }
        .scope-title {
            font-family: var(--font-mono); font-size: 0.68rem; font-weight: 800; color: var(--cyan);
            display: flex; align-items: center; gap: 6px;
        }
        .scope-channel-pills { display: flex; gap: 5px; align-items: center; flex-wrap: wrap; }
        .channel-pill {
            font-size: 0.6rem; font-family: var(--font-mono); font-weight: 700;
            padding: 2px 6px; border-radius: 3px; cursor: pointer; user-select: none;
            border: 1px solid currentColor; transition: all 0.15s;
        }
        .channel-pill.active { background: currentColor; color: #000 !important; }
        .scope-btn {
            background: rgba(255,255,255,0.08); color: var(--text-primary); border: 1px solid rgba(255,255,255,0.2);
            border-radius: 3px; padding: 2px 6px; font-size: 0.6rem; font-family: var(--font-mono);
            cursor: pointer;
        }
        .scope-btn:hover { background: rgba(255,255,255,0.18); }
        .scope-canvas-wrap {
            width: 100%; height: 120px; position: relative; background: #040609;
            border-radius: 4px; border: 1px solid rgba(255,255,255,0.08); overflow: hidden;
        }
        canvas#telemetry-canvas { width: 100%; height: 100%; display: block; }
        .canvas-readout {
            position: absolute; top: 3px; right: 6px; font-family: var(--font-mono);
            font-size: 0.6rem; color: var(--text-muted); background: rgba(0,0,0,0.7);
            padding: 2px 5px; border-radius: 3px; pointer-events: none;
        }

        /* LIVE CAN TABLE */
        .table-card {
            background: var(--panel-bg); border: 1px solid var(--panel-border);
            border-radius: 6px; padding: 7px 10px;
        }
        table { width: 100%; border-collapse: collapse; font-family: var(--font-mono); font-size: 0.6rem; }
        th, td { border: 1px solid rgba(255, 255, 255, 0.06); padding: 3px 5px; text-align: left; }
        th { background: rgba(8, 12, 18, 0.95); color: var(--text-muted); text-transform: uppercase; }

        @media (max-width: 900px) {
            .top-nav-grid { grid-template-columns: 1fr 1fr; }
            .p2-dashboard-grid { grid-template-columns: 1fr; }
            .shift-strip-container { flex-direction: column; gap: 6px; }
        }
        @media (max-width: 600px) {
            body { padding: 6px 8px; }
            .brand-header { flex-direction: column; align-items: flex-start; gap: 4px; }
            .brand-title { font-size: 0.95rem; }
            .top-nav-grid { grid-template-columns: 1fr 1fr; gap: 6px; }
            .nav-card { height: 42px; padding: 0 8px; gap: 6px; }
            .nav-title { font-size: 0.65rem; }
            .metrics-grid-top { grid-template-columns: repeat(2, 1fr); gap: 6px; }
            .gauge-card-val { font-size: 1.1rem; }
            .scope-canvas-wrap { height: 105px; }
            .table-card { overflow-x: auto; -webkit-overflow-scrolling: touch; }
        }
    </style>
</head>
<body>
    <!-- BRAND TITLE -->
    <div class="brand-header">
        <div style="display:flex; flex-direction:column; gap:2px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span class="brand-title">NexusMBD // AI-NATIVE POWERTRAIN ENGINEERING SUITE</span>
                <span style="background:rgba(0,229,255,0.15); color:var(--cyan); border:1px solid var(--cyan); font-family:var(--font-mono); font-size:0.58rem; padding:1px 5px; border-radius:3px; font-weight:800;">v2.6 PRO</span>
            </div>
            <span class="brand-sub">4 AI PILLARS: [MCP] CAN CONTEXT • [RAG] KNOWLEDGE BASE • [AGENTS] SIMULINK MBD • [FINE-TUNING] LLM TELEMETRY</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <a href="/apostila" target="_blank" class="scope-btn" style="color:var(--cyan); border-color:var(--cyan); font-weight:bold; text-decoration:none; padding:3px 8px; font-size:0.65rem; border-radius:4px; display:inline-flex; align-items:center; gap:4px;">
                📖 APOSTILA TÉCNICA
            </a>
            <a href="/slides" target="_blank" class="scope-btn" style="color:var(--amber); border-color:var(--amber); font-weight:bold; text-decoration:none; padding:3px 8px; font-size:0.65rem; border-radius:4px; display:inline-flex; align-items:center; gap:4px;">
                🎬 SLIDES EXECUTIVOS
            </a>
            <div style="display:flex; align-items:center; gap:8px; background:rgba(0,230,118,0.08); border:1px solid rgba(0,230,118,0.25); padding:3px 8px; border-radius:4px;">
                <span class="pulse-dot"></span>
                <span style="font-family:var(--font-mono); font-size:0.62rem; color:var(--green); font-weight:800; letter-spacing:0.5px;">P2 HEV SYSTEM ONLINE</span>
            </div>
        </div>
    </div>

    <!-- TOP 4 SYMMETRICAL AUTOMOTIVE BLOCKS -->
    <div class="top-nav-grid">
        <!-- 1. ARQUITETURA 4 MAINS -->
        <div class="nav-card" style="--card-color: var(--cyan);">
            <svg class="nav-icon" viewBox="0 0 24 24">
                <rect x="3" y="8" width="18" height="10" rx="2" stroke-linecap="round"/>
                <path d="M7 8V5a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v3M10 18v2M14 18v2M3 13h2M19 13h2"/>
                <circle cx="12" cy="13" r="2"/>
            </svg>
            <div class="nav-text-col">
                <span class="nav-label">ARQUITETURA</span>
                <span class="nav-title">4 MAINS MBD</span>
            </div>
        </div>

        <!-- 2. EXPORTAR CSV (DATALOGGER) -->
        <a href="/api/export-csv" class="nav-card nav-btn" style="--card-color: #00b0ff;" download="nexusmbd_can_telemetry.csv">
            <svg class="nav-icon" viewBox="0 0 24 24">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            <div class="nav-text-col">
                <span class="nav-label">DATALOGGER</span>
                <span class="nav-title">EXPORTAR CSV</span>
            </div>
        </a>

        <!-- 3. EXECUTAR MIL (SIMULADOR) -->
        <button class="nav-card nav-btn" id="run-mil-button" type="button" style="--card-color: var(--amber);">
            <svg class="nav-icon" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="9"/>
                <polygon points="10 8 16 12 10 16 10 8" fill="var(--amber)"/>
            </svg>
            <div class="nav-text-col">
                <span class="nav-label">SIMULADOR</span>
                <span class="nav-title" id="mil-btn-text">EXECUTAR MIL</span>
            </div>
        </button>

        <!-- 4. REDE CAN // P2HEV STATUS -->
        <div class="nav-card" style="--card-color: var(--green);">
            <span class="pulse-dot"></span>
            <svg class="nav-icon" viewBox="0 0 24 24">
                <path d="M12 2v6M9 8h6M7 14h10M12 14v8M5 11l2 2M19 11l-2 2"/>
            </svg>
            <div class="nav-text-col">
                <span class="nav-label">REDE CAN</span>
                <span class="nav-title">P2HEV ONLINE</span>
            </div>
        </div>
    </div>

    <!-- SHIFT LIGHTS & GEAR CLUSTER -->
    <div class="shift-strip-container">
        <div class="shift-lights" id="shift-lights-bar">
            <!-- 16 Shift LEDs: 6 green, 6 yellow, 3 red, 1 blue limiter -->
            <div class="led green" id="led-1"></div>
            <div class="led green" id="led-2"></div>
            <div class="led green" id="led-3"></div>
            <div class="led green" id="led-4"></div>
            <div class="led green" id="led-5"></div>
            <div class="led green" id="led-6"></div>
            <div class="led yellow" id="led-7"></div>
            <div class="led yellow" id="led-8"></div>
            <div class="led yellow" id="led-9"></div>
            <div class="led yellow" id="led-10"></div>
            <div class="led yellow" id="led-11"></div>
            <div class="led yellow" id="led-12"></div>
            <div class="led red" id="led-13"></div>
            <div class="led red" id="led-14"></div>
            <div class="led red" id="led-15"></div>
            <div class="led blue" id="led-16"></div>
        </div>
        <div class="gear-indicator-box">
            <div class="gear-current" id="val-gear">1</div>
            <div class="gear-details">
                <span class="clutch-badge" id="val-clutch">C1</span>
                <span style="color:var(--text-muted); font-size:0.55rem;" id="val-preselect">PRE: 2 (C2)</span>
            </div>
        </div>
    </div>

    <!-- MIL PROGRESS & FEEDBACK BANNER -->
    <div class="mil-feedback-banner" id="mil-feedback">
        <div class="mil-banner-row">
            <span id="mil-feedback-message" style="font-weight:bold;">MIL pronto para execucao.</span>
            <div style="display:flex; gap:8px; align-items:center;">
                <button id="btn-open-simulink-direct" class="scope-btn" style="color:var(--cyan); border-color:var(--cyan); font-weight:bold; cursor:pointer;" type="button">
                    ABRIR SIMULINK
                </button>
                <span id="mil-progress-pct" style="color:var(--cyan); font-weight:bold;">0%</span>
            </div>
        </div>
        <div class="mil-progress-track">
            <div class="mil-progress-bar" id="mil-progress-bar"></div>
        </div>
        <div class="mil-banner-row" style="font-size:0.62rem;">
            <span id="mil-feedback-metrics" style="color:var(--green);"></span>
            <span id="mil-model-status" style="color:var(--text-muted);">Simulink Model: MIL_MarleyOS_Powertrain</span>
        </div>
    </div>

    <!-- PRIMARY GAUGES -->
    <div class="metrics-grid-top">
        <div class="gauge-card" style="--card-accent: var(--cyan);">
            <div class="gauge-card-title">Velocidade</div>
            <div class="gauge-card-val" style="color:var(--cyan);">
                <span id="val-speed">0.0</span> <span class="gauge-card-unit">km/h</span>
            </div>
            <div class="gauge-sub-row">
                <span>Gx: <strong id="val-gx">0.00</strong>G</span>
                <span>Gy: <strong id="val-gy">0.00</strong>G</span>
            </div>
        </div>

        <div class="gauge-card" style="--card-accent: var(--green);">
            <div class="gauge-card-title">Potencia Hibrida</div>
            <div class="gauge-card-val" style="color:var(--green);">
                <span id="val-p-total">0.0</span> <span class="gauge-card-unit">kW</span>
            </div>
            <div class="gauge-sub-row">
                <span><span id="val-cv">0</span> cv</span>
                <span style="color:var(--cyan);" id="val-p-em">EM: 0 kW</span>
            </div>
        </div>

        <div class="gauge-card" style="--card-accent: var(--purple);">
            <div class="gauge-card-title">FOC PMSM // Iq</div>
            <div class="gauge-card-val" style="color:var(--purple);">
                <span id="val-iq">0.0</span> <span class="gauge-card-unit">A</span>
            </div>
            <div class="gauge-sub-row">
                <span>Freq: <span id="val-freq">0</span> Hz</span>
                <span>Teto: 250 A</span>
            </div>
        </div>

        <div class="gauge-card" style="--card-accent: var(--amber);">
            <div class="gauge-card-title">ICE 1.5L Miller</div>
            <div class="gauge-card-val" style="color:var(--amber);">
                <span id="val-rpm-ice">0</span> <span class="gauge-card-unit">RPM</span>
            </div>
            <div class="gauge-sub-row">
                <span>Rotor EM: <span id="val-rpm-em" style="color:var(--cyan);">0</span></span>
                <span id="val-delta-rpm" style="color:var(--text-muted);">&Delta; 0</span>
            </div>
        </div>

        <div class="gauge-card" style="--card-accent: #00e676;">
            <div class="gauge-card-title">HV Bateria & Bus</div>
            <div class="gauge-card-val" style="color:#00e676;">
                <span id="val-soc">0.0</span> <span class="gauge-card-unit">%</span>
            </div>
            <div class="gauge-sub-row">
                <span><span id="val-vbus">350</span>V</span>
                <span><span id="val-ibat">0</span>A | <span id="val-range">0</span>km</span>
            </div>
        </div>
    </div>

    <!-- DYNAMIC TOPOLOGY SVG SECTION (RESTORED WITH ACTIVE STATES) -->
    <div class="topology-card">
        <div class="topology-header">
            <span>ARQUITETURA DINAMICA // TOPOLOGIA P2 &amp; e-DCT DUAL-SHAFT</span>
            <span id="topology-status" class="topology-status-badge">MODO: EV_MODE</span>
        </div>
        <div class="topology-container" id="topology-wrapper">
            {{SVG_TOPOLOGY}}
        </div>
    </div>

    <!-- P2 MBD POWERTRAIN DETAILS -->
    <div class="p2-dashboard-grid">
        <!-- DOMAIN 1: TORQUE & PROPULSION -->
        <div class="domain-box">
            <div class="domain-title">
                <span>Split de Torque &amp; Modos</span>
                <span id="val-torque-total" style="color:var(--cyan);">0 Nm</span>
            </div>
            <div class="mode-hero-badge EV_MODE" id="val-mode-hero">EV_MODE</div>
            
            <div class="torque-split-bar">
                <div class="split-thermal" id="bar-t-ice" style="width: 0%;"></div>
                <div class="split-electric" id="bar-t-em" style="width: 100%;"></div>
            </div>
            <div class="split-legend">
                <span style="color:var(--amber);">ICE: <strong id="val-t-ice">0.0</strong> Nm (<span id="val-t-ice-pct">0%</span>)</span>
                <span style="color:var(--green);">EM: <strong id="val-t-em">0.0</strong> Nm (<span id="val-t-em-pct">100%</span>)</span>
            </div>

            <!-- COMPACT RACING PEDALS (REDUCED BY HALF) -->
            <div class="pedals-compact-row">
                <!-- ACCEL -->
                <div class="pedal-item">
                    <div class="pedal-billet throttle" id="pedal-throttle">
                        <div class="billet-hole"></div>
                        <div class="billet-hole"></div>
                        <div class="billet-hole"></div>
                    </div>
                    <div class="pedal-info">
                        <div class="pedal-title-bar">
                            <span style="color:var(--green);">ACEL</span>
                            <span id="val-throttle">0%</span>
                        </div>
                        <div class="pedal-mini-gauge">
                            <div class="pedal-mini-fill" id="fill-throttle" style="background:var(--green);"></div>
                        </div>
                    </div>
                </div>
                <!-- BRAKE -->
                <div class="pedal-item">
                    <div class="pedal-billet brake" id="pedal-brake">
                        <div class="billet-hole"></div>
                        <div class="billet-hole"></div>
                    </div>
                    <div class="pedal-info">
                        <div class="pedal-title-bar">
                            <span style="color:var(--red);">FREIO</span>
                            <span id="val-brake">0%</span>
                        </div>
                        <div class="pedal-mini-gauge">
                            <div class="pedal-mini-fill" id="fill-brake" style="background:var(--red);"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- DOMAIN 2: K0 COUPLING & DUAL-SHAFT DCT -->
        <div class="domain-box">
            <div class="domain-title">
                <span>Dinamica K0 &amp; Transmissao e-DCT</span>
                <span id="val-k0-pressure-text" style="color:var(--amber);">0.0 bar</span>
            </div>

            <div class="k0-coupling-meter">
                <div style="display:flex; justify-content:space-between; font-size:0.62rem; font-family:var(--font-mono);">
                    <span>Escorregamento K0:</span>
                    <span>&Delta;&omega; = <strong id="val-delta-rpm-text" style="color:var(--cyan);">0</strong> RPM</span>
                </div>
                <div class="meter-bar-track">
                    <div class="meter-bar-fill" id="bar-k0-pressure" style="width:0%; background:var(--amber);"></div>
                </div>
                <div class="k0-status-badge OPEN" id="val-k0-phase-badge">FASE 1: SYNC / OPEN (0.5 bar)</div>
            </div>

            <div class="dct-matrix">
                <div class="shaft-col">
                    <span class="shaft-title">EIXO SOLIDO (C1)</span>
                    <div class="gear-nodes">
                        <div class="gear-node" id="gear-node-1">1</div>
                        <div class="gear-node" id="gear-node-3">3</div>
                        <div class="gear-node" id="gear-node-5">5</div>
                    </div>
                </div>
                <div class="shaft-col">
                    <span class="shaft-title">EIXO OCO (C2)</span>
                    <div class="gear-nodes">
                        <div class="gear-node" id="gear-node-2">2</div>
                        <div class="gear-node" id="gear-node-4">4</div>
                        <div class="gear-node" id="gear-node-6">6</div>
                        <div class="gear-node" id="gear-node-R">R</div>
                    </div>
                </div>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.62rem; font-family:var(--font-mono); color:var(--text-muted);">
                <span>Inv. Temp: <strong id="val-temp-inv" style="color:var(--cyan);">45°C</strong></span>
                <span>ASIL Status: <strong style="color:var(--green);">ASIL-D NOMINAL</strong></span>
            </div>
        </div>

        <!-- DOMAIN 3: BSFC & G-BOWL -->
        <div class="domain-box">
            <div class="domain-title">
                <span>Eficiencia BSFC &amp; Forca G</span>
                <span id="val-bsfc" style="color:var(--green);">0 g/kWh</span>
            </div>

            <!-- BSFC SWEET SPOT METER -->
            <div style="background:rgba(0,0,0,0.3); padding:5px 7px; border-radius:4px; border:1px solid rgba(255,255,255,0.06); display:flex; flex-direction:column; gap:3px;">
                <div style="display:flex; justify-content:space-between; font-size:0.62rem; font-family:var(--font-mono);">
                    <span>Consumo Especifico:</span>
                    <span id="val-bsfc-zone" style="color:var(--green); font-weight:bold;">OFF (EV)</span>
                </div>
                <div class="meter-bar-track" style="background:linear-gradient(90deg, #333 0%, #ff9100 20%, #00e676 40%, #ff9100 70%, #ff1744 100%);">
                    <div class="meter-bar-fill" id="bar-bsfc-needle" style="width:0%; background:#fff; box-shadow:0 0 8px #fff; width:3px;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.55rem; color:var(--text-muted); font-family:var(--font-mono);">
                    <span>0</span>
                    <span style="color:var(--green);">SWEET SPOT (230-250)</span>
                    <span>400+</span>
                </div>
            </div>

            <!-- G-BOWL -->
            <div style="display:flex; align-items:center; justify-content:space-around;">
                <div class="g-bowl-circle">
                    <div class="g-cross-h"></div>
                    <div class="g-cross-v"></div>
                    <div class="g-dot" id="g-dot"></div>
                </div>
                <div style="font-family:var(--font-mono); font-size:0.62rem; display:flex; flex-direction:column; gap:2px;">
                    <div>Gx: <strong id="val-gx-bowl" style="color:var(--cyan);">0.00</strong> G</div>
                    <div>Gy: <strong id="val-gy-bowl" style="color:var(--green);">0.00</strong> G</div>
                    <div style="color:var(--text-muted); font-size:0.55rem;">G-BOWL DYNAMICS</div>
                </div>
            </div>
        </div>
    </div>

    <!-- OSCILLOSCOPE INTERACTIVE CANVAS -->
    <div class="oscilloscope-section">
        <div class="scope-header">
            <div class="scope-title">
                <span>&#128200;</span>
                <span>OSCILOSCOPIO DE TELEMETRIA // 60 FPS</span>
            </div>
            <div class="scope-channel-pills">
                <span class="channel-pill active" style="color:var(--cyan);" data-channel="speed_kmh">Velocidade</span>
                <span class="channel-pill active" style="color:var(--green);" data-channel="t_em">Torque EM</span>
                <span class="channel-pill active" style="color:var(--amber);" data-channel="t_ice">Torque ICE</span>
                <span class="channel-pill active" style="color:var(--purple);" data-channel="iq_a">Corrente Iq</span>
                <span class="channel-pill" style="color:#ff5252;" data-channel="k0_press_bar">Pressao K0</span>
                <button class="scope-btn" id="btn-pause-scope" type="button">PAUSAR</button>
                <button class="scope-btn" id="btn-clear-scope" type="button">LIMPAR</button>
            </div>
        </div>
        <div class="scope-canvas-wrap">
            <canvas id="telemetry-canvas"></canvas>
            <div class="canvas-readout" id="scope-cursor-readout">T: -- | V: -- km/h | EM: -- Nm | ICE: -- Nm</div>
        </div>
    </div>

    <!-- LIVE CAN FRAME LOG -->
    <div class="table-card">
        <div style="font-family:var(--font-mono); font-size:0.65rem; font-weight:800; color:var(--cyan); margin-bottom:5px;">
            BUFFER DE TELEMETRIA CAN // RECENT FRAMES
        </div>
        <table>
            <thead>
                <tr>
                    <th>Tempo</th>
                    <th>Vel (km/h)</th>
                    <th>Marcha</th>
                    <th>Modo</th>
                    <th>Rotor EM</th>
                    <th>ICE RPM</th>
                    <th>Split Tem/Tice</th>
                    <th>Iq (A)</th>
                    <th>K0 Press</th>
                    <th>BSFC</th>
                </tr>
            </thead>
            <tbody id="table-body">
                <tr><td colspan="10" style="text-align:center; color:var(--text-muted);">Aguardando telemetria CAN...</td></tr>
            </tbody>
        </table>
    </div>

    <script>
        // CONFIG & STATE
        const MAX_POINTS = 140;
        const telemetryHistory = [];
        let isScopePaused = false;
        let telemetryRequestInFlight = false;
        const channelsVisible = {
            speed_kmh: true,
            t_em: true,
            t_ice: true,
            iq_a: true,
            k0_press_bar: false
        };

        // CANVAS SETUP
        const canvas = document.getElementById('telemetry-canvas');
        const ctx = canvas.getContext('2d');
        function resizeCanvas() {
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        // SHIFT LIGHTS UPDATE LOGIC
        function updateShiftLights(rpm) {
            const minRPM = 1500;
            const maxRPM = 6500;
            const range = maxRPM - minRPM;
            const fraction = Math.max(0, Math.min(1, (rpm - minRPM) / range));
            const litCount = Math.round(fraction * 16);

            for (let i = 1; i <= 16; i++) {
                const led = document.getElementById(`led-${i}`);
                if (i <= litCount) {
                    led.classList.add('on');
                } else {
                    led.classList.remove('on');
                }
            }
        }

        // DUAL-SHAFT DCT MATRIX UPDATE
        function updateDCTMatrix(currentGear, preselectedGear) {
            const gears = ['1', '2', '3', '4', '5', '6', 'R'];
            gears.forEach(g => {
                const node = document.getElementById(`gear-node-${g}`);
                if (node) {
                    node.classList.remove('active', 'preselect');
                    if (g === String(currentGear)) {
                        node.classList.add('active');
                    } else if (g === String(preselectedGear)) {
                        node.classList.add('preselect');
                    }
                }
            });
        }

        // SVG TOPOLOGY REACTIVE HIGHLIGHTS (P2 + K0 + EM + e-DCT)
        function updateSvgClasses(mode, k0State, activeClutch, gear) {
            const ice = document.getElementById('svg-ice');
            const k0 = document.getElementById('svg-k0');
            const em = document.getElementById('svg-em');
            const c1Top = document.getElementById('svg-clutch1-top');
            const c1Bot = document.getElementById('svg-clutch1-bot');
            const c2Top = document.getElementById('svg-clutch2-top');
            const c2Bot = document.getElementById('svg-clutch2-bot');
            const topStatus = document.getElementById('topology-status');
            if (!ice || !k0 || !em) return;

            ice.classList.remove('active-ice');
            k0.classList.remove('active-k0');
            em.classList.remove('active-em', 'active-em-regen');
            if (c1Top) c1Top.classList.remove('active-clutch1');
            if (c1Bot) c1Bot.classList.remove('active-clutch1');
            if (c2Top) c2Top.classList.remove('active-clutch2');
            if (c2Bot) c2Bot.classList.remove('active-clutch2');

            for (let g = 1; g <= 6; g++) {
                const el = document.getElementById('gear-' + g);
                if (el) el.style.filter = 'none';
            }
            const gearR = document.getElementById('gear-r');
            if (gearR) gearR.style.filter = 'none';

            if (activeClutch === 'CLUTCH_1') {
                if (c1Top) c1Top.classList.add('active-clutch1');
                if (c1Bot) c1Bot.classList.add('active-clutch1');
            } else if (activeClutch === 'CLUTCH_2') {
                if (c2Top) c2Top.classList.add('active-clutch2');
                if (c2Bot) c2Bot.classList.add('active-clutch2');
            }

            const activeGearEl = document.getElementById('gear-' + (gear === 'R' ? 'r' : gear));
            if (activeGearEl) activeGearEl.style.filter = 'drop-shadow(0 0 10px #00e5ff)';

            if (topStatus) {
                topStatus.textContent = `MODO: ${mode} [K0: ${k0State} | ${activeClutch} MARCH: ${gear}]`;
            }

            if (mode === 'EV_MODE') {
                em.classList.add('active-em');
                if (topStatus) topStatus.style.borderColor = 'var(--green)';
            } else if (mode === 'P2_HYBRID_BOOST') {
                ice.classList.add('active-ice');
                k0.classList.add('active-k0');
                em.classList.add('active-em');
                if (topStatus) topStatus.style.borderColor = 'var(--cyan)';
            } else if (mode === 'REGEN_BRAKE') {
                em.classList.add('active-em-regen');
                if (topStatus) topStatus.style.borderColor = 'var(--red)';
            }
        }

        // DRAW OSCILLOSCOPE
        function drawOscilloscope() {
            if (!canvas.width || !canvas.height) return;
            const w = canvas.width;
            const h = canvas.height;

            ctx.clearRect(0, 0, w, h);

            // Background Grid Lines
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            for (let x = 0; x < w; x += 40) {
                ctx.moveTo(x, 0); ctx.lineTo(x, h);
            }
            for (let y = 0; y < h; y += 25) {
                ctx.moveTo(0, y); ctx.lineTo(w, y);
            }
            ctx.stroke();

            // Zero line
            const midY = h * 0.7;
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
            ctx.beginPath(); ctx.moveTo(0, midY); ctx.lineTo(w, midY); ctx.stroke();

            if (telemetryHistory.length < 2) return;

            // Draw Channels
            const stepX = w / (MAX_POINTS - 1);

            function plotSeries(channelKey, color, scaleMin, scaleMax) {
                if (!channelsVisible[channelKey]) return;
                ctx.strokeStyle = color;
                ctx.lineWidth = 2;
                ctx.beginPath();

                for (let i = 0; i < telemetryHistory.length; i++) {
                    const val = Number(telemetryHistory[i][channelKey]) || 0;
                    const norm = (val - scaleMin) / (scaleMax - scaleMin);
                    const py = h - (norm * (h - 14) + 7);
                    const px = i * stepX;
                    if (i === 0) ctx.moveTo(px, py);
                    else ctx.lineTo(px, py);
                }
                ctx.stroke();
            }

            plotSeries('speed_kmh', '#00e5ff', 0, 160);
            plotSeries('t_em', '#00e676', -80, 260);
            plotSeries('t_ice', '#ff9100', 0, 200);
            plotSeries('iq_a', '#b388ff', -100, 260);
            plotSeries('k0_press_bar', '#ff5252', 0, 20);
        }

        // FETCH TELEMETRY LOOP
        async function fetchTelemetry() {
            if (telemetryRequestInFlight) return;
            telemetryRequestInFlight = true;
            try {
                const res = await fetch('/api/telemetry');
                if (!res.ok) return;
                const data = await res.json();
                if (!data.rows || !data.rows.length) return;

                const last = data.rows[data.rows.length - 1];

                // Append to history buffer if not paused
                if (!isScopePaused) {
                    telemetryHistory.push(last);
                    if (telemetryHistory.length > MAX_POINTS) telemetryHistory.shift();
                    drawOscilloscope();
                }

                // 1. Shift Lights & Gear
                const rpmIce = parseFloat(last.rpm_ice || 0);
                updateShiftLights(rpmIce);
                document.getElementById('val-gear').textContent = last.gear || '1';
                
                const clutchBadge = document.getElementById('val-clutch');
                clutchBadge.textContent = last.active_clutch === 'CLUTCH_2' ? 'C2' : 'C1';
                if (last.active_clutch === 'CLUTCH_2') {
                    clutchBadge.classList.add('c2');
                } else {
                    clutchBadge.classList.remove('c2');
                }
                document.getElementById('val-preselect').textContent = `PRE: ${last.preselected_gear || '2'} (${last.preselected_clutch || 'C2'})`;
                updateDCTMatrix(last.gear || '1', last.preselected_gear || '2');

                // 2. Primary Gauges
                document.getElementById('val-speed').textContent = parseFloat(last.speed_kmh || 0).toFixed(1);
                document.getElementById('val-gx').textContent = parseFloat(last.gx || 0).toFixed(2);
                document.getElementById('val-gy').textContent = parseFloat(last.gy || 0).toFixed(2);
                document.getElementById('val-p-total').textContent = parseFloat(last.p_total_kw || 0).toFixed(1);
                document.getElementById('val-cv').textContent = Math.round(last.p_total_cv || 0);
                document.getElementById('val-p-em').textContent = `EM: ${parseFloat(last.p_em_kw || 0).toFixed(1)} kW`;
                document.getElementById('val-iq').textContent = parseFloat(last.iq_a || 0).toFixed(1);
                document.getElementById('val-freq').textContent = Math.round(last.elec_freq_hz || 0);
                document.getElementById('val-rpm-ice').textContent = Math.round(rpmIce);
                document.getElementById('val-rpm-em').textContent = Math.round(last.rpm_em || 0);
                document.getElementById('val-delta-rpm').textContent = `Δ ${Math.round(last.delta_rpm || 0)}`;
                document.getElementById('val-soc').textContent = parseFloat(last.soc_pct || 0).toFixed(1);
                document.getElementById('val-vbus').textContent = Math.round(last.bus_voltage_v || 350);
                document.getElementById('val-ibat').textContent = Math.round(last.battery_current_a || 0);
                document.getElementById('val-range').textContent = parseFloat(last.ev_range_km || 0).toFixed(1);

                // 3. Torque Split
                const totalTorque = parseFloat(last.torque_nm || 0);
                const tIce = Math.max(0, parseFloat(last.t_ice || 0));
                const tEm = parseFloat(last.t_em || 0);
                document.getElementById('val-torque-total').textContent = `${totalTorque.toFixed(0)} Nm`;
                document.getElementById('val-t-ice').textContent = tIce.toFixed(1);
                document.getElementById('val-t-em').textContent = tEm.toFixed(1);

                const denom = Math.max(1, tIce + Math.abs(tEm));
                const icePct = Math.round((tIce / denom) * 100);
                const emPct = 100 - icePct;
                document.getElementById('val-t-ice-pct').textContent = `${icePct}%`;
                document.getElementById('val-t-em-pct').textContent = `${emPct}%`;
                document.getElementById('bar-t-ice').style.width = `${icePct}%`;
                document.getElementById('bar-t-em').style.width = `${emPct}%`;

                // Mode Hero Badge
                const modeBadge = document.getElementById('val-mode-hero');
                const modeStr = last.modo_propulsao || 'EV_MODE';
                modeBadge.textContent = modeStr;
                modeBadge.className = `mode-hero-badge ${modeStr}`;

                // 4. Compact Racing Pedals (Reduced by half)
                const throttle = Math.max(0, Math.min(100, parseFloat(last.throttle_pct || 0)));
                const brake = Math.max(0, Math.min(100, parseFloat(last.brake_pct || 0)));
                document.getElementById('val-throttle').textContent = `${throttle.toFixed(0)}%`;
                document.getElementById('val-brake').textContent = `${brake.toFixed(0)}%`;
                document.getElementById('fill-throttle').style.width = `${throttle}%`;
                document.getElementById('fill-brake').style.width = `${brake}%`;

                // 5. K0 Dynamics
                const k0Press = parseFloat(last.k0_press_bar || 0);
                document.getElementById('val-k0-pressure-text').textContent = `${k0Press.toFixed(1)} bar`;
                document.getElementById('val-delta-rpm-text').textContent = Math.round(last.delta_rpm || 0);
                document.getElementById('bar-k0-pressure').style.width = `${Math.min(100, (k0Press / 18.0) * 100)}%`;
                
                const k0Badge = document.getElementById('val-k0-phase-badge');
                const k0State = last.k0_state || 'OPEN';
                k0Badge.textContent = `${last.k0_phase || 'FASE 1: SYNC'} [${k0State}]`;
                k0Badge.className = `k0-status-badge ${k0State}`;

                document.getElementById('val-temp-inv').textContent = `${parseFloat(last.temp_inv_c || 45).toFixed(1)}°C`;

                // 6. BSFC Sweet Spot
                const bsfc = parseFloat(last.bsfc_g_kwh || 0);
                document.getElementById('val-bsfc').textContent = `${bsfc.toFixed(0)} g/kWh`;
                document.getElementById('val-bsfc-zone').textContent = last.bsfc_zone || 'OFF';
                const bsfcNeedlePos = Math.max(0, Math.min(100, (bsfc / 400.0) * 100));
                document.getElementById('bar-bsfc-needle').style.marginLeft = `${bsfcNeedlePos}%`;

                // 7. G-Bowl
                const gx = Math.max(-1.5, Math.min(1.5, parseFloat(last.gx || 0)));
                const gy = Math.max(-1.5, Math.min(1.5, parseFloat(last.gy || 0)));
                document.getElementById('val-gx-bowl').textContent = gx.toFixed(2);
                document.getElementById('val-gy-bowl').textContent = gy.toFixed(2);
                document.getElementById('g-dot').style.transform = `translate(${gy * 20}px, ${-gx * 20}px)`;

                // 8. UPDATE SVG TOPOLOGY STATES
                updateSvgClasses(modeStr, k0State, last.active_clutch || 'CLUTCH_1', last.gear || '1');

                // 9. Table Rows
                let rowsHtml = '';
                for (let i = data.rows.length - 1; i >= Math.max(0, data.rows.length - 5); i--) {
                    const r = data.rows[i];
                    rowsHtml += `<tr>
                        <td>${r.timestamp_s}s</td>
                        <td><strong>${r.speed_kmh}</strong></td>
                        <td>${r.gear} (${r.active_clutch === 'CLUTCH_2' ? 'C2' : 'C1'})</td>
                        <td><span style="color:var(--cyan);">${r.modo_propulsao}</span></td>
                        <td>${r.rpm_em}</td>
                        <td>${r.rpm_ice}</td>
                        <td>${r.t_em || r.torque_nm} / ${r.t_ice || 0}</td>
                        <td style="color:var(--purple);">${r.iq_a || 0} A</td>
                        <td style="color:var(--amber);">${r.k0_press_bar} bar</td>
                        <td style="color:var(--green);">${r.bsfc_g_kwh || 0}</td>
                    </tr>`;
                }
                document.getElementById('table-body').innerHTML = rowsHtml;

            } catch (err) {
                console.error('Falha na telemetria CAN:', err);
            } finally {
                telemetryRequestInFlight = false;
            }
        }

        // INTERVAL FOR TELEMETRY
        setInterval(fetchTelemetry, 150);

        // CHANNEL PILLS TOGGLE
        document.querySelectorAll('.channel-pill').forEach(pill => {
            pill.addEventListener('click', () => {
                const ch = pill.getAttribute('data-channel');
                channelsVisible[ch] = !channelsVisible[ch];
                pill.classList.toggle('active', channelsVisible[ch]);
                drawOscilloscope();
            });
        });

        // OSCILLOSCOPE PAUSE & CLEAR
        const pauseBtn = document.getElementById('btn-pause-scope');
        pauseBtn.addEventListener('click', () => {
            isScopePaused = !isScopePaused;
            pauseBtn.textContent = isScopePaused ? 'CONTINUAR' : 'PAUSAR';
            pauseBtn.style.color = isScopePaused ? 'var(--green)' : 'var(--text-primary)';
        });
        document.getElementById('btn-clear-scope').addEventListener('click', () => {
            telemetryHistory.length = 0;
            drawOscilloscope();
        });

        // CANVAS HOVER & TOUCH READOUT FOR MOBILE
        function handlePointer(clientX) {
            if (!telemetryHistory.length) return;
            const rect = canvas.getBoundingClientRect();
            const mouseX = clientX - rect.left;
            const frac = Math.max(0, Math.min(1, mouseX / canvas.width));
            const idx = Math.min(telemetryHistory.length - 1, Math.floor(frac * telemetryHistory.length));
            const pt = telemetryHistory[idx];
            if (pt) {
                document.getElementById('scope-cursor-readout').textContent = 
                    `T: ${pt.timestamp_s}s | V: ${pt.speed_kmh} km/h | EM: ${pt.t_em || pt.torque_nm} Nm | ICE: ${pt.t_ice || 0} Nm | Iq: ${pt.iq_a || 0}A`;
            }
        }
        canvas.addEventListener('mousemove', (e) => handlePointer(e.clientX));
        canvas.addEventListener('touchmove', (e) => {
            if (e.touches && e.touches[0]) handlePointer(e.touches[0].clientX);
        }, { passive: true });
        canvas.addEventListener('touchstart', (e) => {
            if (e.touches && e.touches[0]) handlePointer(e.touches[0].clientX);
        }, { passive: true });

        // RUN MIL JOB BUTTON WITH ANIMATED PROGRESS BAR & SIMULINK MODEL LAUNCH
                // DIRECT OPEN SIMULINK BUTTON
        const btnOpenDirect = document.getElementById('btn-open-simulink-direct');
        if (btnOpenDirect) {
            btnOpenDirect.addEventListener('click', async () => {
                const feedback = document.getElementById('mil-feedback');
                const msg = document.getElementById('mil-feedback-message');
                const modelStatus = document.getElementById('mil-model-status');
                feedback.classList.add('visible');
                msg.textContent = 'Iniciando MATLAB & Simulink (splash aparecendo na tela)...';
                modelStatus.textContent = 'Carregando MIL_MarleyOS_Powertrain (~15-20s)...';
                try {
                    await fetch('/api/open-model', { method: 'POST' });
                    msg.textContent = '\u2705 Comando enviado! Janela do Simulink abrindo na sua Área de Trabalho.';
                } catch(e) {
                    msg.textContent = 'Erro ao enviar comando de abertura.';
                }
            });
        }

        // RUN MIL JOB BUTTON WITH ANIMATED PROGRESS BAR & SIMULINK MODEL LAUNCH
        async function runMil() {
            const btn = document.getElementById('run-mil-button');
            const btnText = document.getElementById('mil-btn-text');
            const feedback = document.getElementById('mil-feedback');
            const msg = document.getElementById('mil-feedback-message');
            const pct = document.getElementById('mil-progress-pct');
            const bar = document.getElementById('mil-progress-bar');
            const metricsSpan = document.getElementById('mil-feedback-metrics');
            const modelStatus = document.getElementById('mil-model-status');

            btn.disabled = true;
            btnText.textContent = 'EXECUTANDO...';
            feedback.classList.add('visible');
            msg.textContent = '1/4: Inicializando MATLAB e abrindo modelo no Simulink...';
            pct.textContent = '8%';
            bar.style.width = '8%';
            metricsSpan.textContent = 'Aguardando solvers e interface gráfica...';
            modelStatus.textContent = 'Splash do MATLAB em carregamento na tela...';

            // Start smooth progress animation timer (~20s duration)
            let progress = 8;
            const progressTimer = setInterval(() => {
                if (progress < 90) {
                    progress += Math.floor(Math.random() * 5) + 3;
                    progress = Math.min(90, progress);
                    pct.textContent = `${progress}%`;
                    bar.style.width = `${progress}%`;

                    if (progress > 15 && progress <= 45) {
                        msg.textContent = '2/4: Simulando Solvers 4 Mains (COMUNICACAO -> SOFTECU -> MDL)...';
                        modelStatus.textContent = 'Solvers MBD em cálculo contínuo...';
                    } else if (progress > 45 && progress <= 75) {
                        msg.textContent = '3/4: Solvers finalizando & abrindo janela gráfica do Simulink...';
                        modelStatus.textContent = 'Janela do Simulink ativa na sua Área de Trabalho!';
                    } else if (progress > 75) {
                        msg.textContent = '3/4: Consolidando métricas de telemetria e datasets...';
                    }
                }
            }, 700);

            try {
                // Trigger model opening and simulation run
                fetch('/api/open-model', { method: 'POST' }).catch(() => {});

                const postRes = await fetch('/api/run-mil', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ stopTime: 1 })
                });
                if (!postRes.ok) throw new Error('Falha ao disparar simulacao MIL');

                let status = 'running';
                while (status === 'running' || status === 'queued') {
                    await new Promise(r => setTimeout(r, 1000));
                    const pollRes = await fetch('/api/run-mil');
                    const pollData = await pollRes.json();
                    status = pollData.status;

                    if (status === 'passed') {
                        clearInterval(progressTimer);
                        bar.style.width = '100%';
                        pct.textContent = '100%';
                        msg.textContent = '\u2705 4/4: SIMULACAO CONCLUIDA (PASSED) & MODELO ABERTO NO SIMULINK';
                        modelStatus.textContent = 'Simulink: Model Loaded & Active na sua Área de Trabalho';
                        const m = pollData.result && pollData.result.metrics ? pollData.result.metrics : {};
                        metricsSpan.textContent = `Peak Iq: ${m.peakIqA || 0} A | BSFC: ${m.bsfcGPerKwh || 0} g/kWh | Gx: ${m.peakGx || 0}G | Resíduo: ${m.peakDecelerationResidual || 0}`;
                        break;
                    } else if (status === 'failed') {
                        clearInterval(progressTimer);
                        bar.style.width = '100%';
                        pct.textContent = 'FALHA';
                        msg.textContent = '\u274C SIMULACAO MIL FALHOU';
                        metricsSpan.textContent = pollData.message || 'Verifique os logs do MATLAB.';
                        break;
                    }
                }
            } catch (err) {
                clearInterval(progressTimer);
                msg.textContent = `Erro: ${err.message}`;
            } finally {
                btn.disabled = false;
                btnText.textContent = 'EXECUTAR MIL';
            }
        }
        document.getElementById('run-mil-button').addEventListener('click', runMil);

        // INITIAL CALL
        fetchTelemetry();
    </script>
</body>
</html>"""
    return template.replace("{{SVG_TOPOLOGY}}", svg_content)


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


class ClusterHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        req_path = urlparse(self.path).path
        if req_path == "/api/open-model":
            threading.Thread(target=open_simulink_model, daemon=True).start()
            self._send_json(200, {"status": "ok", "message": "Modelo MIL sendo aberto no MATLAB/Simulink."})
            return

        if req_path != "/api/run-mil":
            self.send_error(404, "Arquivo nao encontrado")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        request_body = self.rfile.read(content_length) if content_length else b"{}"
        try:
            request = json.loads(request_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_error(400, "JSON invalido")
            return

        try:
            stop_time = float(request.get("stopTime", 1))
        except (TypeError, ValueError):
            self.send_error(400, "stopTime invalido")
            return
        if not 0 < stop_time <= 120:
            self.send_error(400, "stopTime deve estar entre 0 e 120 segundos")
            return

        run_id = uuid.uuid4().hex
        generate_default_dbc()
        with MIL_RUN_LOCK:
            MIL_RUN_STATE.update({
                "run_id": run_id,
                "status": "queued",
                "message": "Execucao MIL enfileirada.",
                "result": None,
            })
        # Open model and run simulation
        threading.Thread(target=open_simulink_model, daemon=True).start()
        threading.Thread(target=run_mil_job, args=(run_id, stop_time), daemon=True).start()
        self._send_json(202, dict(MIL_RUN_STATE))

    def do_GET(self):
        req_path = urlparse(self.path).path
        if not req_path.startswith("/"):
            req_path = "/" + req_path

        if req_path == "/api/telemetry":
            rows = read_telemetry_rows()
            payload = json.dumps({"rows": rows}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)

        elif req_path == "/api/p2hev/status":
            payload = json.dumps({
                "model": "P2HybridVehicle",
                "model_path": P2HEV_MODEL_PATH,
                "available": os.path.exists(P2HEV_MODEL_PATH),
                "matlab_release": "R2026a",
                "logging_contract": "Dataset/logsout",
                "signals": P2HEV_SIGNALS,
                "telemetry_source": CSV_PATH,
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)

        elif req_path == "/api/run-mil":
            with MIL_RUN_LOCK:
                payload = json.dumps(dict(MIL_RUN_STATE)).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)

        elif req_path == "/api/export-csv":
            if os.path.exists(CSV_PATH):
                with open(CSV_PATH, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", "attachment; filename=nexusmbd_can_telemetry.csv")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "Arquivo CSV nao encontrado")

        elif req_path == "/topology.svg":
            if os.path.exists(SVG_PATH):
                with open(SVG_PATH, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "SVG nao encontrado")

        elif req_path == "/slides":
            slides_path = os.path.join(ROOT_DIR, "course", "slides", "deck_01_intro_mbd_ai.html")
            if os.path.exists(slides_path):
                with open(slides_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "Slides nao encontrados")

        elif req_path in ("/apostila", "/docs"):
            self.send_response(302)
            self.send_header("Location", "/site/")
            self.end_headers()

        elif req_path.startswith("/site"):
            rel_site_path = req_path[len("/site"):]
            if not rel_site_path or rel_site_path.endswith("/"):
                rel_site_path = rel_site_path.rstrip("/") + "/index.html"
            rel_site_path = rel_site_path.lstrip("/")
            file_disk_path = os.path.join(ROOT_DIR, "site", rel_site_path.replace("/", os.sep))
            if os.path.exists(file_disk_path) and os.path.isfile(file_disk_path):
                mime_type = "text/html; charset=utf-8"
                if file_disk_path.endswith(".css"):
                    mime_type = "text/css"
                elif file_disk_path.endswith(".js"):
                    mime_type = "application/javascript"
                elif file_disk_path.endswith(".svg"):
                    mime_type = "image/svg+xml"
                elif file_disk_path.endswith(".png"):
                    mime_type = "image/png"
                elif file_disk_path.endswith(".woff2"):
                    mime_type = "font/woff2"
                with open(file_disk_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", mime_type)
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "Arquivo de documentacao nao encontrado")

        elif req_path in ("/", "/index.html", ""):
            html = get_html_page()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        elif req_path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
        else:
            self.send_error(404, "Arquivo nao encontrado")

    def log_message(self, format, *args):
        pass

    def _send_json(self, status, value):
        payload = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)


def run_mil_job(run_id, stop_time):
    model_dir = os.path.join(ROOT_DIR, "module_3_agents_simulink")
    harness_dir = os.path.join(ROOT_DIR, "Model")
    mcp_dir = os.path.join(ROOT_DIR, "module_2_mcp")
    matlab_expression = (
        "cd('%s'); addpath('%s'); addpath('%s'); addpath('%s'); "
        "modelName='MIL_MarleyOS_Powertrain'; stopTime=%.15g; "
        "inputData=load_dbc_signals('%s'); "
        "result=run_4mains_mil(modelName, stopTime, inputData); "
        "disp(result.metrics.signalCount);"
    ) % (
        model_dir.replace("'", "''"),
        model_dir.replace("'", "''"),
        harness_dir.replace("'", "''"),
        mcp_dir.replace("'", "''"),
        stop_time,
        CSV_PATH.replace("'", "''"),
    )
    with MIL_RUN_LOCK:
        MIL_RUN_STATE.update({"status": "running", "message": "MATLAB MIL em execucao."})
    try:
        completed = subprocess.run(
            [MATLAB_BIN, "-batch", matlab_expression],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            timeout=max(120, int(stop_time * 60)),
            check=False,
        )
        status = "passed" if completed.returncode == 0 else "failed"
        result = {
            "returncode": completed.returncode,
            "stdout": completed.stdout[-4000:],
            "stderr": completed.stderr[-4000:],
        }
        for line in completed.stdout.splitlines():
            if line.startswith("MARLEYOS_METRICS="):
                try:
                    result["metrics"] = json.loads(line.split("=", 1)[1])
                except json.JSONDecodeError:
                    result["metrics"] = {"parse_error": True}
        with MIL_RUN_LOCK:
            MIL_RUN_STATE.update({
                "status": status,
                "message": "Execucao MIL concluida." if status == "passed" else "Execucao MIL falhou.",
                "result": result,
            })
    except (OSError, subprocess.TimeoutExpired) as error:
        with MIL_RUN_LOCK:
            MIL_RUN_STATE.update({
                "status": "failed",
                "message": "Nao foi possivel executar o MATLAB MIL.",
                "result": {"error": str(error)},
            })


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NexusMBD Cockpit Server")
    parser.add_argument("--host", default="", help="Host address to bind")
    parser.add_argument("--port", type=int, default=PORT, help="Port to listen on")
    args = parser.parse_args()
    with ThreadingTCPServer((args.host, args.port), ClusterHandler) as httpd:
        display_host = args.host if args.host and args.host != "0.0.0.0" else "localhost"
        print(f"Servidor ativo em http://{display_host}:{args.port}")
        httpd.serve_forever()
