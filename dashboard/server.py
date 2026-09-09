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


def normalize_p2hev_row(row):
    """Map P2HEV Dataset export columns to the cockpit's existing contract."""
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
        "temp_inv_c": "0",
        "modo_propulsao": "P2_HEV" if float(row.get("EngineOn", 0) or 0) else "EV_MODE",
        "status_motor": "NOMINAL",
        "bus_voltage_v": row.get("BusVoltage", "0"),
        "battery_current_a": row.get("HVBatCurrent", "0"),
        "engine_torque_request_nm": row.get("EngTrqReq", "0"),
        "speed_setpoint_kmh": row.get("SpeedSetPoint", "0"),
    }


def read_telemetry_rows():
    rows = []
    for _ in range(3):
        if not os.path.exists(CSV_PATH):
            break
        try:
            with open(CSV_PATH, "r", encoding="utf-8") as telemetry_file:
                raw_rows = list(csv.DictReader(telemetry_file))
            rows = [normalize_p2hev_row(row) for row in raw_rows]
            break
        except (OSError, UnicodeDecodeError, ValueError):
            time.sleep(0.005)
    return rows

HTML_PAGE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarleyOS | Race Cockpit P2</title>
    <style>
        :root {
            --carbon: #080a0f;
            --panel: #0e131d;
            --border: rgba(0, 210, 255, 0.28);
            --cyan: #00d2ff;
            --green: #00e676;
            --red: #ff1744;
            --yellow: #ffd600;
            --orange: #ff9100;
            --text: #f0f6fc;
            --text-dim: #7d8590;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'SF Pro Display', -apple-system, sans-serif;
            background: radial-gradient(circle at 50% 20%, #151b28 0%, var(--carbon) 80%);
            color: var(--text);
            padding: 10px;
            min-height: 100vh;
        }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid rgba(0, 210, 255, 0.2); padding-bottom: 6px; margin-bottom: 10px; }
        .brand { font-family: monospace; font-weight: 900; font-size: 1.1rem; color: var(--cyan); }
        .header-actions { display: flex; align-items: center; gap: 8px; }
        .mil-run-button {
            background: rgba(255,145,0,0.16); color: var(--orange); border: 1px solid var(--orange);
            border-radius: 4px; padding: 4px 8px; font-size: 0.65rem; font-weight: bold; font-family: monospace;
            cursor: pointer;
        }
        .mil-run-button:disabled { opacity: 0.55; cursor: wait; }
        .mil-feedback {
            display: none; margin: 0 0 10px; padding: 7px 10px; border: 1px solid var(--border);
            background: rgba(14,19,29,0.95); border-radius: 6px; font-family: monospace; font-size: 0.7rem;
        }
        .mil-feedback.visible { display: flex; justify-content: space-between; gap: 12px; align-items: center; }
        .mil-metrics { color: var(--text-dim); }
        .btn-logger {
            background: rgba(0, 210, 255, 0.15); color: var(--cyan); border: 1px solid var(--cyan);
            border-radius: 4px; padding: 3px 8px; font-size: 0.65rem; font-weight: bold; font-family: monospace;
            cursor: pointer; text-decoration: none; transition: background 0.2s;
        }
        .btn-logger:active { background: var(--cyan); color: #000; }
        .live-tag { font-family: monospace; font-size: 0.68rem; font-weight: bold; background: rgba(0,230,118,0.12); color: var(--green); border: 1px solid var(--green); border-radius: 4px; padding: 2px 6px; }

        .cluster-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(95px, 1fr)); gap: 6px; margin-bottom: 10px; }
        .telemetry-card { background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 6px 8px; position: relative; overflow: hidden; }
        .telemetry-card::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; background: var(--cyan); opacity: 0.7; }
        .card-title { font-size: 0.6rem; color: var(--text-dim); text-transform: uppercase; font-weight: 700; }
        .card-val { font-size: 1.15rem; font-family: monospace; font-weight: 800; margin-top: 2px; }

        /* PEDALEIRA & G-BOWL CONTAINER */
        .controls-row { display: grid; grid-template-columns: 2fr 1.2fr; gap: 8px; margin-bottom: 10px; }
        .pedal-box { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 8px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
        .pedal-unit { display: flex; flex-direction: column; align-items: center; perspective: 600px; }
        .pedal-header { display: flex; justify-content: space-between; width: 100%; font-size: 0.65rem; font-weight: 800; font-family: monospace; margin-bottom: 4px; }
        .pedal-stage { width: 100%; height: 65px; background: #07090e; border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; position: relative; display: flex; justify-content: center; align-items: center; }
        
        .pedal-plate {
            width: 48px; height: 56px; border-radius: 6px; position: relative;
            transform-origin: bottom center; transition: transform 0.1s ease-out;
            display: flex; flex-direction: column; justify-content: space-evenly; align-items: center;
            border: 2px solid #a0aec0; background: linear-gradient(145deg, #2d3748, #1a202c);
        }
        .pedal-grip { width: 30px; height: 4px; background: #111; border-radius: 2px; }
        .brake-plate { border-color: var(--red); }
        .throttle-plate { border-color: var(--green); }
        .pedal-gauge { width: 100%; height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; margin-top: 4px; overflow: hidden; }
        .pedal-gauge-fill { height: 100%; width: 0%; transition: width 0.1s ease; }

        /* G-FORCE METER (G-BOWL) */
        .g-bowl-box { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 6px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; }
        .g-bowl-header { font-size: 0.65rem; font-weight: 800; color: var(--cyan); font-family: monospace; text-transform: uppercase; width: 100%; display: flex; justify-content: space-between; }
        .g-circle {
            width: 65px; height: 65px; border-radius: 50%; border: 1.5px solid rgba(0, 210, 255, 0.4);
            position: relative; background: radial-gradient(circle, rgba(0,210,255,0.05) 0%, rgba(0,0,0,0.7) 100%);
            display: flex; justify-content: center; align-items: center; margin: 4px 0;
        }
        .g-cross-h { position: absolute; width: 100%; height: 1px; background: rgba(255,255,255,0.15); }
        .g-cross-v { position: absolute; height: 100%; width: 1px; background: rgba(255,255,255,0.15); }
        .g-dot {
            width: 10px; height: 10px; border-radius: 50%; background: var(--cyan);
            position: absolute; transform: translate(0px, 0px); box-shadow: 0 0 8px var(--cyan);
            transition: transform 0.15s ease-out;
        }
        .g-readout { font-size: 0.65rem; font-family: monospace; color: var(--text); font-weight: bold; }

        /* BATERIA */
        .battery-widget { display: flex; align-items: center; gap: 5px; margin-top: 2px; }
        .battery-icon { width: 30px; height: 14px; border: 2px solid var(--green); border-radius: 3px; padding: 1px; position: relative; display: flex; align-items: center; }
        .battery-icon::after { content: ''; position: absolute; right: -4px; width: 2px; height: 6px; background: var(--green); }
        .battery-level { height: 100%; width: 75%; background: var(--green); transition: width 0.3s ease; }

        table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 0.62rem; margin-top: 8px; }
        th, td { border: 1px solid rgba(255, 255, 255, 0.07); padding: 3px 4px; text-align: left; }
        th { background: rgba(14, 19, 29, 0.95); color: var(--text-dim); text-transform: uppercase; }

        .topology-card { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 8px; margin-top: 10px; }
        .topology-header { display: flex; justify-content: space-between; align-items: center; font-size: 0.68rem; color: var(--cyan); font-weight: 800; font-family: monospace; margin-bottom: 4px; }
        .topology-container { width: 100%; height: 230px; display: flex; justify-content: center; }
        object { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <div class="header">
        <div class="brand">MarleyOS // RACING TELEMETRY</div>
        <div class="header-actions">
            <a href="/api/export-csv" class="btn-logger" download="marleyos_can_telemetry.csv">💾 EXPORTAR CSV</a>
            <button class="mil-run-button" id="run-mil-button" type="button">🚀 EXECUTAR MIL (MATLAB)</button>
            <div class="live-tag" id="p2hev-status">P2HEV OFFLINE</div>
        </div>
    </div>

    <div class="mil-feedback" id="mil-feedback" role="status" aria-live="polite">
        <span id="mil-feedback-message">MIL aguardando execução.</span>
        <span class="mil-metrics" id="mil-feedback-metrics"></span>
    </div>

    <div class="cluster-grid">
        <div class="telemetry-card"><div class="card-title">Velocidade</div><div class="card-val" style="color:var(--cyan);"><span id="val-speed">0.0</span> <span style="font-size:0.55rem; color:var(--text-dim);">km/h</span></div></div>
        <div class="telemetry-card"><div class="card-title">Câmbio e-DCT</div><div class="card-val" style="color:var(--cyan);"><span id="val-gear">1</span> <span style="font-size:0.6rem; color:var(--red);" id="val-clutch">[C1]</span></div></div>
        <div class="telemetry-card"><div class="card-title">Rotor EM</div><div class="card-val" style="color:var(--green);"><span id="val-rpm-em">0</span> <span style="font-size:0.55rem; color:var(--text-dim);">RPM</span></div></div>
        <div class="telemetry-card"><div class="card-title">ICE RPM</div><div class="card-val"><span id="val-rpm-ice">0</span> <span style="font-size:0.55rem; color:var(--text-dim);">RPM</span></div></div>
        <div class="telemetry-card"><div class="card-title">K0 Linha</div><div class="card-val" style="color:var(--orange);"><span id="val-k0-press">0.0</span> <span style="font-size:0.55rem; color:var(--text-dim);">bar</span></div><div id="val-k0-state" style="font-size:0.55rem; color:var(--text-dim);">OPEN</div></div>
        
        <div class="telemetry-card">
            <div class="card-title">Bateria HV</div>
            <div class="battery-widget">
                <div class="battery-icon" id="bat-box"><div id="bat-level" class="battery-level"></div></div>
                <div class="card-val" style="margin-top:0; font-size:0.95rem;" id="soc-text-wrap"><span id="val-soc">0.0</span>%</div>
            </div>
            <div style="font-size:0.55rem; color:var(--text-dim); margin-top:2px;">Range: <span id="val-range" style="color:var(--green); font-weight:bold;">0.0</span> km</div>
        </div>
    </div>

    <!-- CONTROLES: PEDAIS E MEDIDOR DE FORÇA G -->
    <div class="controls-row">
        <div class="pedal-box">
            <div class="pedal-unit">
                <div class="pedal-header"><span style="color:var(--red);">FREIO</span><span id="brake-pct-txt" style="color:var(--red);">0%</span></div>
                <div class="pedal-stage"><div id="pedal-brake" class="pedal-plate brake-plate"><div class="pedal-grip"></div><div class="pedal-grip"></div></div></div>
                <div class="pedal-gauge"><div id="brake-gauge" class="pedal-gauge-fill" style="background:var(--red);"></div></div>
            </div>
            <div class="pedal-unit">
                <div class="pedal-header"><span style="color:var(--green);">TPS</span><span id="throttle-pct-txt" style="color:var(--green);">0%</span></div>
                <div class="pedal-stage"><div id="pedal-throttle" class="pedal-plate throttle-plate"><div class="pedal-grip"></div><div class="pedal-grip"></div></div></div>
                <div class="pedal-gauge"><div id="throttle-gauge" class="pedal-gauge-fill" style="background:var(--green);"></div></div>
            </div>
        </div>

        <div class="g-bowl-box">
            <div class="g-bowl-header"><span>G-METER</span><span id="g-mag" style="color:var(--cyan);">0.00 G</span></div>
            <div class="g-circle">
                <div class="g-cross-h"></div><div class="g-cross-v"></div>
                <div id="g-dot" class="g-dot"></div>
            </div>
            <div class="g-readout">X: <span id="gx-val">0.00</span> | Y: <span id="gy-val">0.00</span></div>
        </div>
    </div>

    <!-- TABELA CAN -->
    <table>
        <thead><tr><th>s</th><th>km/h</th><th>Marcha</th><th>Gx</th><th>Gy</th><th>EM(RPM)</th><th>TPS</th><th>Freio</th><th>Modo</th></tr></thead>
        <tbody id="table-body"></tbody>
    </table>

    <!-- ESQUEMÁTICO e-DCT -->
    <div class="topology-card">
        <div class="topology-header">
            <span>Esquemático e-DCT Dual-Shaft</span>
            <span id="topology-status" style="color: var(--green); font-size: 0.65rem;">MODO: EV_MODE</span>
        </div>
        <div class="topology-container">
            <object id="svg-obj" type="image/svg+xml" data="/topology.svg"></object>
        </div>
    </div>

    <script>
        function updateSvgClasses(mode, k0State, activeClutch, gear) {
            const obj = document.getElementById('svg-obj');
            if (!obj || !obj.contentDocument) return;
            const svgDoc = obj.contentDocument;

            const ice = svgDoc.getElementById('svg-ice');
            const k0 = svgDoc.getElementById('svg-k0');
            const em = svgDoc.getElementById('svg-em');
            const c1Top = svgDoc.getElementById('svg-clutch1-top');
            const c1Bot = svgDoc.getElementById('svg-clutch1-bot');
            const c2Top = svgDoc.getElementById('svg-clutch2-top');
            const c2Bot = svgDoc.getElementById('svg-clutch2-bot');
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
                const el = svgDoc.getElementById('gear-' + g);
                if (el) el.style.filter = 'none';
            }

            if (activeClutch === 'CLUTCH_1') {
                if (c1Top) c1Top.classList.add('active-clutch1');
                if (c1Bot) c1Bot.classList.add('active-clutch1');
            } else if (activeClutch === 'CLUTCH_2') {
                if (c2Top) c2Top.classList.add('active-clutch2');
                if (c2Bot) c2Bot.classList.add('active-clutch2');
            }

            const activeGearEl = svgDoc.getElementById('gear-' + gear);
            if (activeGearEl) activeGearEl.style.filter = 'drop-shadow(0 0 8px #00d2ff)';

            if (topStatus) topStatus.innerText = 'MODO: ' + mode + ' [K0: ' + k0State + ' | ' + activeClutch + ' MARCH: ' + gear + ']';

            if (mode === 'EV_MODE') {
                em.classList.add('active-em');
                if (topStatus) topStatus.style.color = 'var(--green)';
            } else if (mode === 'P2_HYBRID_BOOST') {
                ice.classList.add('active-ice');
                em.classList.add('active-em');
                if (k0State === 'LOCKED' || k0State === 'SLIP') k0.classList.add('active-k0');
                if (topStatus) topStatus.style.color = 'var(--cyan)';
            } else if (mode === 'REGEN_BRAKE') {
                em.classList.add('active-em-regen');
                if (topStatus) topStatus.style.color = 'var(--red)';
            }
        }

        let telemetryRequestInFlight = false;
        let milPollTimer = null;

        function setMilFeedback(message, color, metrics) {
            const feedback = document.getElementById('mil-feedback');
            feedback.classList.add('visible');
            feedback.style.borderColor = color;
            document.getElementById('mil-feedback-message').innerText = message;
            document.getElementById('mil-feedback-metrics').innerText = metrics || '';
        }

        async function pollMilStatus() {
            const response = await fetch('/api/run-mil');
            const state = await response.json();
            if (state.status === 'queued' || state.status === 'running') {
                setMilFeedback('Executando simulação...', 'var(--orange)');
                milPollTimer = setTimeout(pollMilStatus, 1000);
                return;
            }
            const button = document.getElementById('run-mil-button');
            button.disabled = false;
            if (state.status === 'passed') {
                const metrics = state.result && state.result.metrics ? state.result.metrics : {};
                const iq = metrics.peakIqA == null ? 'n/d' : metrics.peakIqA;
                const gx = metrics.peakGx == null ? 'n/d' : metrics.peakGx;
                setMilFeedback('MIL Aprovado', 'var(--green)', `iq pico: ${iq} A | Gx máx: ${gx} G | logsout: OK`);
            } else if (state.status === 'failed') {
                setMilFeedback('Falha no MIL', 'var(--red)', state.message || 'Verifique o log MATLAB.');
            }
        }

        async function runMil() {
            const button = document.getElementById('run-mil-button');
            button.disabled = true;
            setMilFeedback('Executando simulação...', 'var(--orange)');
            try {
                const response = await fetch('/api/run-mil', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({stopTime: 1})
                });
                if (!response.ok) throw new Error('HTTP ' + response.status);
                await pollMilStatus();
            } catch (error) {
                button.disabled = false;
                setMilFeedback('Falha no MIL', 'var(--red)', error.message);
            }
        }

        async function fetchP2HEVStatus() {
            try {
                const res = await fetch('/api/p2hev/status');
                const data = await res.json();
                const status = document.getElementById('p2hev-status');
                if (data.available) {
                    status.innerText = 'P2HEV ' + data.matlab_release;
                    status.style.color = 'var(--green)';
                } else {
                    status.innerText = 'P2HEV OFFLINE';
                    status.style.color = 'var(--red)';
                }
            } catch (err) {
                console.error('Falha status P2HEV:', err);
            }
        }

        async function fetchTelemetry() {
            if (telemetryRequestInFlight) return;
            telemetryRequestInFlight = true;
            try {
                const res = await fetch('/api/telemetry');
                if (!res.ok) return;
                const data = await res.json();
                if (!data.rows || data.rows.length === 0) return;

                const last = data.rows[data.rows.length - 1];
                document.getElementById('val-speed').innerText = last.speed_kmh || '0.0';
                document.getElementById('val-gear').innerText = last.gear || '1';

                const activeClutch = last.active_clutch || 'CLUTCH_1';
                const clutchLabel = activeClutch === 'CLUTCH_1' ? '[C1]' : '[C2]';
                const clutchElem = document.getElementById('val-clutch');
                clutchElem.innerText = clutchLabel;
                clutchElem.style.color = activeClutch === 'CLUTCH_1' ? 'var(--red)' : 'var(--green)';

                document.getElementById('val-rpm-em').innerText = last.rpm_em || '0';
                document.getElementById('val-rpm-ice').innerText = last.rpm_ice || '0';
                document.getElementById('val-k0-press').innerText = last.k0_press_bar || '0.0';
                document.getElementById('val-range').innerText = last.ev_range_km || '0.0';

                // Pedais
                const throttleVal = parseFloat(last.throttle_pct || '0');
                const brakeVal = parseFloat(last.brake_pct || '0');
                document.getElementById('throttle-pct-txt').innerText = throttleVal.toFixed(0) + '%';
                document.getElementById('brake-pct-txt').innerText = brakeVal.toFixed(0) + '%';
                document.getElementById('throttle-gauge').style.width = throttleVal + '%';
                document.getElementById('brake-gauge').style.width = brakeVal + '%';

                document.getElementById('pedal-throttle').style.transform = `rotateX(${(throttleVal/100)*28}deg)`;
                document.getElementById('pedal-brake').style.transform = `rotateX(${(brakeVal/100)*28}deg)`;

                // G-Bowl Calculation (-1.5G a +1.5G escala no raio de 26px)
                const gx = parseFloat(last.gx || '0');
                const gy = parseFloat(last.gy || '0');
                document.getElementById('gx-val').innerText = gx.toFixed(2);
                document.getElementById('gy-val').innerText = gy.toFixed(2);
                const gMag = Math.sqrt(gx*gx + gy*gy);
                document.getElementById('g-mag').innerText = gMag.toFixed(2) + ' G';

                const posX = Math.max(-26, Math.min(26, gy * 20));
                const posY = Math.max(-26, Math.min(26, -gx * 20));
                const gDot = document.getElementById('g-dot');
                gDot.style.transform = `translate(${posX}px, ${posY}px)`;
                if (gMag > 0.6) gDot.style.background = 'var(--red)';
                else if (gMag > 0.3) gDot.style.background = 'var(--yellow)';
                else gDot.style.background = 'var(--cyan)';

                // K0
                const k0StateElem = document.getElementById('val-k0-state');
                const k0State = last.k0_state || 'OPEN';
                k0StateElem.innerText = k0State;
                k0StateElem.style.color = k0State === 'LOCKED' ? 'var(--green)' : (k0State === 'SLIP' ? 'var(--yellow)' : 'var(--text-dim)');

                // Bateria
                const socVal = parseFloat(last.soc_pct || '0');
                document.getElementById('val-soc').innerText = socVal.toFixed(1);
                const batLevel = document.getElementById('bat-level');
                batLevel.style.width = Math.max(5, Math.min(100, socVal)) + '%';
                let batColor = socVal < 20 ? 'var(--red)' : (socVal < 50 ? 'var(--yellow)' : 'var(--green)');
                batLevel.style.background = batColor;
                document.getElementById('bat-box').style.borderColor = batColor;
                document.getElementById('soc-text-wrap').style.color = batColor;

                const mode = last.modo_propulsao || 'NOMINAL';
                updateSvgClasses(mode, k0State, activeClutch, last.gear || '1');

                let rowsHtml = '';
                for (let r of data.rows) {
                    rowsHtml += `<tr><td>${r.timestamp_s}</td><td>${r.speed_kmh}</td><td>${r.gear}</td><td>${r.gx}</td><td>${r.gy}</td><td>${r.rpm_em}</td><td>${r.throttle_pct}%</td><td>${r.brake_pct}%</td><td>${r.modo_propulsao}</td></tr>`;
                }
                document.getElementById('table-body').innerHTML = rowsHtml;
            } catch (err) {
                console.error('Falha CAN:', err);
            } finally {
                telemetryRequestInFlight = false;
            }
        }
        setInterval(fetchTelemetry, 500);
        document.getElementById('run-mil-button').addEventListener('click', runMil);
        fetchP2HEVStatus();
        fetchTelemetry();
    </script>
</body>
</html>"""

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

class ClusterHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/run-mil":
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
        threading.Thread(target=run_mil_job, args=(run_id, stop_time), daemon=True).start()
        self._send_json(202, dict(MIL_RUN_STATE))

    def do_GET(self):
        if self.path == "/api/telemetry":
            rows = read_telemetry_rows()

            payload = json.dumps({"rows": rows}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)

        elif self.path == "/api/p2hev/status":
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

        elif self.path == "/api/run-mil":
            with MIL_RUN_LOCK:
                payload = json.dumps(dict(MIL_RUN_STATE)).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)

        elif self.path == "/api/export-csv":
            if os.path.exists(CSV_PATH):
                with open(CSV_PATH, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", "attachment; filename=marleyos_can_telemetry.csv")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "Arquivo CSV nao encontrado")

        elif self.path == "/topology.svg":
            if os.path.exists(SVG_PATH):
                with open(SVG_PATH, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "SVG nao encontrado")

        elif self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
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
    with ThreadingTCPServer(("", PORT), ClusterHandler) as httpd:
        print(f"Servidor ativo em http://localhost:{PORT}")
        httpd.serve_forever()
