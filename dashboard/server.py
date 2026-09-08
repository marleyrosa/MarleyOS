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
    <title>MarleyOS | Automotive Cluster</title>
    <style>
        :root {
            --bg: #07090e; --surface: rgba(18, 24, 38, 0.85); --border: rgba(0, 210, 255, 0.25);
            --cyan: #00d2ff; --green: #00e676; --red: #ff3366; --yellow: #ffd600; --orange: #ff9900; --text: #e6edf3; --text-dim: #8b949e;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); padding: 12px; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 8px; margin-bottom: 12px; }
        .brand { font-weight: 800; font-size: 1.05rem; color: var(--cyan); }
        .grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(105px, 1fr)); gap: 8px; margin-bottom: 12px; }
        .stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 8px 10px; }
        .stat-title { font-size: 0.65rem; color: var(--text-dim); text-transform: uppercase; }
        .stat-val { font-size: 1.15rem; font-weight: 700; margin-top: 3px; }
        
        .battery-widget { display: flex; align-items: center; gap: 6px; margin-top: 4px; }
        .battery-icon { width: 32px; height: 16px; border: 2px solid var(--green); border-radius: 3px; padding: 1px; position: relative; display: flex; align-items: center; }
        .battery-icon::after { content: ''; position: absolute; right: -5px; width: 3px; height: 7px; background: var(--green); border-radius: 0 2px 2px 0; }
        .battery-level { height: 100%; width: 75%; background: var(--green); border-radius: 1px; transition: width 0.3s ease, background 0.3s ease; }

        table { width: 100%; border-collapse: collapse; font-size: 0.65rem; margin-top: 12px; }
        th, td { border: 1px solid rgba(255, 255, 255, 0.08); padding: 4px 4px; text-align: left; }
        th { background: rgba(15, 22, 36, 0.9); color: var(--text-dim); text-transform: uppercase; }
        .topology-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 10px; margin-top: 14px; }
        .topology-header { display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: var(--cyan); font-weight: 700; text-transform: uppercase; margin-bottom: 6px; }
        .topology-container { width: 100%; height: 175px; display: flex; justify-content: center; }
        object { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <div class="header">
        <div class="brand">MarleyOS Cockpit // Trem de Força</div>
        <div id="live-indicator" style="font-size: 0.72rem; color: var(--green);">CLUSTER ONLINE (LIVE)</div>
    </div>
    <div class="grid-stats">
        <div class="stat-card"><div class="stat-title">Velocidade</div><div class="stat-val" style="color:var(--cyan);"><span id="val-speed">0.0</span> <span style="font-size:0.6rem; color:var(--text-dim);">km/h</span></div></div>
        <div class="stat-card"><div class="stat-title">Marcha / Câmbio</div><div class="stat-val" style="color:var(--cyan);"><span id="val-gear">G1</span> <span style="font-size:0.6rem; color:var(--orange);" id="val-active-clutch">[K1]</span></div></div>
        <div class="stat-card"><div class="stat-title">Tacômetro EM</div><div class="stat-val" style="color:var(--cyan);"><span id="val-rpm-em">0</span> <span style="font-size:0.6rem; color:var(--text-dim);">RPM</span></div></div>
        <div class="stat-card"><div class="stat-title">Tacômetro ICE</div><div class="stat-val" style="color:var(--text);"><span id="val-rpm-ice">0</span> <span style="font-size:0.6rem; color:var(--text-dim);">RPM</span></div></div>
        <div class="stat-card"><div class="stat-title">Embreagem K0</div><div class="stat-val" style="color:var(--orange);"><span id="val-k0-press">0.0</span> <span style="font-size:0.6rem; color:var(--text-dim);">bar</span></div><div id="val-k0-state" style="font-size:0.6rem; color:var(--text-dim);">OPEN</div></div>
        
        <div class="stat-card">
            <div class="stat-title">Bateria Pack</div>
            <div class="battery-widget">
                <div class="battery-icon" id="bat-box">
                    <div id="bat-level" class="battery-level"></div>
                </div>
                <div class="stat-val" style="margin-top:0; font-size:1.05rem;" id="soc-text-wrap"><span id="val-soc">0.0</span>%</div>
            </div>
            <div style="font-size:0.6rem; color:var(--text-dim); margin-top:2px;">Autonomia: <span id="val-range" style="color:var(--green); font-weight:700;">0.0</span> km</div>
        </div>
    </div>

    <table>
        <thead><tr><th>Tempo (s)</th><th>km/h</th><th>Marcha</th><th>Embreagem</th><th>EM (RPM)</th><th>ICE (RPM)</th><th>Torque</th><th>Modo</th></tr></thead>
        <tbody id="table-body"></tbody>
    </table>

    <div class="topology-card">
        <div class="topology-header">
            <span>Esquemático DCT: K0, K1, K2 & K3</span>
            <span id="topology-status" style="color: var(--green); font-size: 0.68rem;">MODO: EV_MODE</span>
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

            // Reset geral
            ice.classList.remove('active-ice');
            k0.classList.remove('active-k0-engaged');
            em.classList.remove('active-em-drive', 'active-em-regen');
            if (k1) k1.classList.remove('active-clutch-gear');
            if (k2) k2.classList.remove('active-clutch-gear');
            if (k3) k3.classList.remove('active-clutch-gear');
            if (flowIceK0) flowIceK0.classList.remove('active-flow');
            if (flowK0Em) flowK0Em.classList.remove('active-flow');

            // Ativação da embreagem de marcha específica
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
                document.getElementById('val-active-clutch').innerText = '[' + (last.k_clutch_active || 'K1') + ']';
                document.getElementById('val-rpm-em').innerText = last.rpm_em || '0';
                document.getElementById('val-rpm-ice').innerText = last.rpm_ice || '0';
                document.getElementById('val-k0-press').innerText = last.k0_press_bar || '0.0';
                document.getElementById('val-range').innerText = last.ev_range_km || '0.0';

                const k0StateElem = document.getElementById('val-k0-state');
                const k0State = last.k0_state || 'OPEN';
                k0StateElem.innerText = k0State;
                if (k0State === 'LOCKED') k0StateElem.style.color = 'var(--green)';
                else if (k0State === 'SLIP') k0StateElem.style.color = 'var(--yellow)';
                else k0StateElem.style.color = 'var(--text-dim)';

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
                    rowsHtml += `<tr><td>${r.timestamp_s}</td><td>${r.speed_kmh}</td><td>${r.gear}</td><td>${r.k_clutch_active}</td><td>${r.rpm_em}</td><td>${r.rpm_ice}</td><td>${r.torque_nm}</td><td>${r.modo_propulsao}</td></tr>`;
                }
                document.getElementById('table-body').innerHTML = rowsHtml;
            } catch (err) {
                console.error('Erro CAN:', err);
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
