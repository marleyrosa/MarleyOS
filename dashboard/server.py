import http.server
import socketserver
import os
import csv
import json

PORT = 8080
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")
SVG_PATH = os.path.join(ROOT_DIR, "module_1_rag", "knowledge_base", "p2_powertrain_topology.svg")

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
            font-family: 'SF Pro Display', -apple-system, 'Segoe UI', Roboto, sans-serif;
            background: radial-gradient(circle at 50% 20%, #151b28 0%, var(--carbon) 80%);
            color: var(--text);
            padding: 12px;
            min-height: 100vh;
        }
        .header {
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 2px solid rgba(0, 210, 255, 0.2); padding-bottom: 8px; margin-bottom: 12px;
        }
        .brand { font-family: monospace; font-weight: 900; font-size: 1.15rem; letter-spacing: 1px; color: var(--cyan); text-shadow: 0 0 10px rgba(0,210,255,0.4); }
        .live-tag { font-family: monospace; font-size: 0.72rem; font-weight: bold; background: rgba(0,230,118,0.12); color: var(--green); border: 1px solid var(--green); border-radius: 4px; padding: 2px 6px; }

        .cluster-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 8px; margin-bottom: 12px; }
        .telemetry-card { background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 8px 10px; position: relative; overflow: hidden; }
        .telemetry-card::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; background: var(--cyan); opacity: 0.7; }
        .card-title { font-size: 0.62rem; color: var(--text-dim); text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; }
        .card-val { font-size: 1.25rem; font-family: monospace; font-weight: 800; margin-top: 2px; }

        /* PEDALEIRA ESPORTIVA DE COMPETIÇÃO */
        .pedal-box {
            background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
            padding: 10px; margin-bottom: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px;
        }
        .pedal-unit { display: flex; flex-direction: column; overflow: hidden; align-items: center; perspective: 600px; }
        .pedal-header { display: flex; justify-content: space-between; width: 100%; font-size: 0.7rem; font-weight: 800; font-family: monospace; margin-bottom: 6px; }
        .pedal-stage { width: 100%; height: 80px; background: #07090e; border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; position: relative; display: flex; justify-content: center; align-items: center; overflow: hidden; }
        
        /* Chapa de Alumínio do Pedal */
        .pedal-plate {
            width: 58px; height: 68px; border-radius: 6px; position: relative;
            transform-origin: bottom center; transition: transform 0.1s ease-out, box-shadow 0.1s ease-out;
            display: flex; flex-direction: column; overflow: hidden; justify-content: space-evenly; align-items: center;
            border: 2px solid #a0aec0; background: linear-gradient(145deg, #2d3748, #1a202c);
            box-shadow: 0 6px 10px rgba(0,0,0,0.8);
        }
        .pedal-grip { width: 40px; height: 5px; background: #111; border-radius: 2px; }
        .brake-plate { border-color: var(--red); }
        .throttle-plate { border-color: var(--green); }

        /* Barra de Curso Lateral do Pedal */
        .pedal-gauge { width: 100%; height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; margin-top: 6px; overflow: hidden; }
        .pedal-gauge-fill { height: 100%; width: 0%; transition: width 0.1s ease; }

        /* ÍCONE DE BATERIA */
        .battery-widget { display: flex; align-items: center; gap: 6px; margin-top: 3px; }
        .battery-icon { width: 34px; height: 16px; border: 2px solid var(--green); border-radius: 3px; padding: 1px; position: relative; display: flex; align-items: center; }
        .battery-icon::after { content: ''; position: absolute; right: -5px; width: 3px; height: 7px; background: var(--green); border-radius: 0 2px 2px 0; }
        .battery-level { height: 100%; width: 75%; background: var(--green); border-radius: 1px; transition: width 0.3s ease, background 0.3s ease; }

        table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 0.65rem; margin-top: 10px; }
        th, td { border: 1px solid rgba(255, 255, 255, 0.07); padding: 4px 5px; text-align: left; }
        th { background: rgba(14, 19, 29, 0.95); color: var(--text-dim); text-transform: uppercase; }

        .topology-card { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 10px; margin-top: 12px; }
        .topology-header { display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: var(--cyan); font-weight: 800; text-transform: uppercase; font-family: monospace; margin-bottom: 6px; }
        .topology-container { width: 100%; height: 195px; display: flex; justify-content: center; }
        object { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <div class="header">
        <div class="brand">MarleyOS // RACING TELEMETRY</div>
        <div class="live-tag">LIVE CAN BUS</div>
    </div>

    <!-- MOSTRADORES SUPERIORES ESTILO INSTRUMENTAÇÃO DIGITAL -->
    <div class="cluster-grid">
        <div class="telemetry-card"><div class="card-title">Velocidade</div><div class="card-val" style="color:var(--cyan);"><span id="val-speed">0.0</span> <span style="font-size:0.6rem; color:var(--text-dim);">km/h</span></div></div>
        <div class="telemetry-card"><div class="card-title">Câmbio DCT</div><div class="card-val" style="color:var(--cyan);"><span id="val-gear">G1</span> <span style="font-size:0.65rem; color:var(--orange);" id="val-clutch">[K1]</span></div></div>
        <div class="telemetry-card"><div class="card-title">Rotor EM</div><div class="card-val" style="color:var(--green);"><span id="val-rpm-em">0</span> <span style="font-size:0.55rem; color:var(--text-dim);">RPM</span></div></div>
        <div class="telemetry-card"><div class="card-title">Virabrequim ICE</div><div class="card-val"><span id="val-rpm-ice">0</span> <span style="font-size:0.55rem; color:var(--text-dim);">RPM</span></div></div>
        <div class="telemetry-card"><div class="card-title">K0 Linha</div><div class="card-val" style="color:var(--orange);"><span id="val-k0-press">0.0</span> <span style="font-size:0.55rem; color:var(--text-dim);">bar</span></div><div id="val-k0-state" style="font-size:0.58rem; color:var(--text-dim);">OPEN</div></div>
        
        <div class="telemetry-card">
            <div class="card-title">Bateria HV</div>
            <div class="battery-widget">
                <div class="battery-icon" id="bat-box"><div id="bat-level" class="battery-level"></div></div>
                <div class="card-val" style="margin-top:0; font-size:1.0rem;" id="soc-text-wrap"><span id="val-soc">0.0</span>%</div>
            </div>
            <div style="font-size:0.55rem; color:var(--text-dim); margin-top:2px;">Autonomia: <span id="val-range" style="color:var(--green); font-weight:bold;">0.0</span> km</div>
        </div>
    </div>

    <!-- PEDALEIRA FÍSICA ANIMADA (ACELERADOR & FREIO/REGEN) -->
    <div class="pedal-box">
        <!-- Pedal de Freio -->
        <div class="pedal-unit">
            <div class="pedal-header"><span style="color:var(--red);">[ FREIO / REGEN ]</span><span id="brake-pct-txt" style="color:var(--red);">0.0%</span></div>
            <div class="pedal-stage">
                <div id="pedal-brake" class="pedal-plate brake-plate">
                    <div class="pedal-grip"></div><div class="pedal-grip"></div><div class="pedal-grip"></div>
                </div>
            </div>
            <div class="pedal-gauge"><div id="brake-gauge" class="pedal-gauge-fill" style="background:var(--red);"></div></div>
        </div>

        <!-- Pedal de Acelerador -->
        <div class="pedal-unit">
            <div class="pedal-header"><span style="color:var(--green);">[ ACELERADOR TPS ]</span><span id="throttle-pct-txt" style="color:var(--green);">0.0%</span></div>
            <div class="pedal-stage">
                <div id="pedal-throttle" class="pedal-plate throttle-plate">
                    <div class="pedal-grip"></div><div class="pedal-grip"></div><div class="pedal-grip"></div>
                </div>
            </div>
            <div class="pedal-gauge"><div id="throttle-gauge" class="pedal-gauge-fill" style="background:var(--green);"></div></div>
        </div>
    </div>

    <!-- HISTÓRICO CAN -->
    <table>
        <thead><tr><th>s</th><th>km/h</th><th>Marcha</th><th>EM (RPM)</th><th>ICE (RPM)</th><th>Torque</th><th>TPS</th><th>Brake</th><th>Modo</th></tr></thead>
        <tbody id="table-body"></tbody>
    </table>

    <!-- ESQUEMÁTICO DCT E K0 -->
    <div class="topology-card">
        <div class="topology-header">
            <span>Esquemático DCT: K0, K1, K2 & K3</span>
            <span id="topology-status" style="color: var(--green); font-size: 0.65rem;">MODO: EV_MODE</span>
        </div>
        <div class="topology-container">
            <object id="svg-obj" type="image/svg+xml" data="/topology.svg"></object>
        </div>
    </div>

    <script>
        function updateSvgClasses(mode, k0State, activeClutch) {
            const obj = document.getElementById('svg-obj');
            if (!obj || !obj.contentDocument) return;
            const svgDoc = obj.contentDocument;

            const ice = svgDoc.getElementById('svg-ice');
            const k0 = svgDoc.getElementById('svg-k0');
            const em = svgDoc.getElementById('svg-em');
            const k1 = svgDoc.getElementById('svg-k1');
            const k2 = svgDoc.getElementById('svg-k2');
            const k3 = svgDoc.getElementById('svg-k3');
            const flowIceK0 = svgDoc.getElementById('svg-flow-ice-k0');
            const flowK0Em = svgDoc.getElementById('svg-flow-k0-em');
            const topStatus = document.getElementById('topology-status');
            if (!ice || !k0 || !em) return;

            ice.classList.remove('active-ice');
            k0.classList.remove('active-k0-engaged');
            em.classList.remove('active-em-drive', 'active-em-regen');
            if (k1) k1.classList.remove('active-clutch-gear');
            if (k2) k2.classList.remove('active-clutch-gear');
            if (k3) k3.classList.remove('active-clutch-gear');
            if (flowIceK0) flowIceK0.classList.remove('active-flow');
            if (flowK0Em) flowK0Em.classList.remove('active-flow');

            if (activeClutch === 'K1' && k1) k1.classList.add('active-clutch-gear');
            else if (activeClutch === 'K2' && k2) k2.classList.add('active-clutch-gear');
            else if (activeClutch === 'K3' && k3) k3.classList.add('active-clutch-gear');

            if (topStatus) topStatus.innerText = 'MODO: ' + mode + ' [K0: ' + k0State + ' | ' + activeClutch + ' ATIVA]';

            if (mode === 'EV_MODE') {
                em.classList.add('active-em-drive');
                if (topStatus) topStatus.style.color = 'var(--green)';
            } else if (mode === 'P2_HYBRID_BOOST') {
                ice.classList.add('active-ice');
                em.classList.add('active-em-drive');
                if (k0State === 'LOCKED' || k0State === 'SLIP') {
                    k0.classList.add('active-k0-engaged');
                    if (flowIceK0) flowIceK0.classList.add('active-flow');
                    if (flowK0Em) flowK0Em.classList.add('active-flow');
                }
                if (topStatus) topStatus.style.color = 'var(--cyan)';
            } else if (mode === 'REGEN_BRAKE') {
                em.classList.add('active-em-regen');
                if (topStatus) topStatus.style.color = 'var(--red)';
            }
        }

        async function fetchTelemetry() {
            try {
                const res = await fetch('/api/telemetry');
                if (!res.ok) return;
                const data = await res.json();
                if (!data.rows || data.rows.length === 0) return;

                const last = data.rows[data.rows.length - 1];
                document.getElementById('val-speed').innerText = last.speed_kmh || '0.0';
                document.getElementById('val-gear').innerText = last.gear || 'G1';
                document.getElementById('val-clutch').innerText = '[' + (last.k_clutch_active || 'K1') + ']';
                document.getElementById('val-rpm-em').innerText = last.rpm_em || '0';
                document.getElementById('val-rpm-ice').innerText = last.rpm_ice || '0';
                document.getElementById('val-k0-press').innerText = last.k0_press_bar || '0.0';
                document.getElementById('val-range').innerText = last.ev_range_km || '0.0';

                // Dinâmica dos Pedais de Acelerador e Freio
                const throttleVal = parseFloat(last.throttle_pct || '0');
                const brakeVal = parseFloat(last.brake_pct || '0');

                document.getElementById('throttle-pct-txt').innerText = throttleVal.toFixed(1) + '%';
                document.getElementById('brake-pct-txt').innerText = brakeVal.toFixed(1) + '%';

                document.getElementById('throttle-gauge').style.width = throttleVal + '%';
                document.getElementById('brake-gauge').style.width = brakeVal + '%';

                // Deformação angular 3D simulando o pedal sendo pressionado
                const throttleAngle = (throttleVal / 100.0) * 32.0; // Até 32 graus
                const brakeAngle = (brakeVal / 100.0) * 32.0;

                const throttlePedal = document.getElementById('pedal-throttle');
                const brakePedal = document.getElementById('pedal-brake');

                throttlePedal.style.transform = `rotateX(${throttleAngle}deg) translateZ(-${throttleVal * 0.15}px)`;
                brakePedal.style.transform = `rotateX(${brakeAngle}deg) translateZ(-${brakeVal * 0.15}px)`;

                if (throttleVal > 5) throttlePedal.style.boxShadow = '0 0 14px rgba(0, 230, 118, 0.4)';
                else throttlePedal.style.boxShadow = '0 6px 10px rgba(0,0,0,0.8)';

                if (brakeVal > 5) brakePedal.style.boxShadow = '0 0 14px rgba(255, 23, 68, 0.4)';
                else brakePedal.style.boxShadow = '0 6px 10px rgba(0,0,0,0.8)';

                // Status de K0
                const k0StateElem = document.getElementById('val-k0-state');
                const k0State = last.k0_state || 'OPEN';
                k0StateElem.innerText = k0State;
                if (k0State === 'LOCKED') k0StateElem.style.color = 'var(--green)';
                else if (k0State === 'SLIP') k0StateElem.style.color = 'var(--yellow)';
                else k0StateElem.style.color = 'var(--text-dim)';

                // Bateria HV
                const socVal = parseFloat(last.soc_pct || '0');
                document.getElementById('val-soc').innerText = socVal.toFixed(1);
                
                const batLevel = document.getElementById('bat-level');
                const batBox = document.getElementById('bat-box');
                const socWrap = document.getElementById('soc-text-wrap');
                
                batLevel.style.width = Math.max(5, Math.min(100, socVal)) + '%';
                let batColor = 'var(--green)';
                if (socVal < 20) batColor = 'var(--red)';
                else if (socVal < 50) batColor = 'var(--yellow)';
                
                batLevel.style.background = batColor;
                batBox.style.borderColor = batColor;
                socWrap.style.color = batColor;

                const mode = last.modo_propulsao || 'NOMINAL';
                const activeClutch = last.k_clutch_active || 'K1';
                updateSvgClasses(mode, k0State, activeClutch);

                let rowsHtml = '';
                for (let r of data.rows) {
                    rowsHtml += `<tr><td>${r.timestamp_s}</td><td>${r.speed_kmh}</td><td>${r.gear}</td><td>${r.rpm_em}</td><td>${r.rpm_ice}</td><td>${r.torque_nm}</td><td>${r.throttle_pct}%</td><td>${r.brake_pct}%</td><td>${r.modo_propulsao}</td></tr>`;
                }
                document.getElementById('table-body').innerHTML = rowsHtml;
            } catch (err) {
                console.error('Falha CAN:', err);
            }
        }
        setInterval(fetchTelemetry, 300);
        fetchTelemetry();
    </script>
</body>
</html>"""

class ClusterHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/telemetry":
            rows = []
            if os.path.exists(CSV_PATH):
                try:
                    with open(CSV_PATH, "r", encoding="utf-8") as f:
                        rows = list(csv.DictReader(f))
                except Exception:
                    rows = []

            payload = json.dumps({"rows": rows}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)

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

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ClusterHandler) as httpd:
        print(f"Servidor ativo em http://localhost:{PORT}")
        httpd.serve_forever()
