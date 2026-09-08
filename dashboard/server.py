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
            font-family: 'SF Pro Display', -apple-system, sans-serif;
            background: radial-gradient(circle at 50% 20%, #151b28 0%, var(--carbon) 80%);
            color: var(--text);
            padding: 10px;
            min-height: 100vh;
        }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid rgba(0, 210, 255, 0.2); padding-bottom: 6px; margin-bottom: 10px; }
        .brand { font-family: monospace; font-weight: 900; font-size: 1.1rem; color: var(--cyan); }
        .live-tag { font-family: monospace; font-size: 0.7rem; font-weight: bold; background: rgba(0,230,118,0.12); color: var(--green); border: 1px solid var(--green); border-radius: 4px; padding: 2px 6px; }

        .cluster-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(95px, 1fr)); gap: 6px; margin-bottom: 10px; }
        .telemetry-card { background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 6px 8px; position: relative; overflow: hidden; }
        .telemetry-card::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; background: var(--cyan); opacity: 0.7; }
        .card-title { font-size: 0.6rem; color: var(--text-dim); text-transform: uppercase; font-weight: 700; }
        .card-val { font-size: 1.15rem; font-family: monospace; font-weight: 800; margin-top: 2px; }

        /* PEDALEIRA */
        .pedal-box { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 8px; margin-bottom: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .pedal-unit { display: flex; flex-direction: column; align-items: center; perspective: 600px; }
        .pedal-header { display: flex; justify-content: space-between; width: 100%; font-size: 0.68rem; font-weight: 800; font-family: monospace; margin-bottom: 4px; }
        .pedal-stage { width: 100%; height: 68px; background: #07090e; border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; position: relative; display: flex; justify-content: center; align-items: center; }
        
        .pedal-plate {
            width: 52px; height: 58px; border-radius: 6px; position: relative;
            transform-origin: bottom center; transition: transform 0.1s ease-out;
            display: flex; flex-direction: column; justify-content: space-evenly; align-items: center;
            border: 2px solid #a0aec0; background: linear-gradient(145deg, #2d3748, #1a202c);
        }
        .pedal-grip { width: 34px; height: 4px; background: #111; border-radius: 2px; }
        .brake-plate { border-color: var(--red); }
        .throttle-plate { border-color: var(--green); }
        .pedal-gauge { width: 100%; height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; margin-top: 4px; overflow: hidden; }
        .pedal-gauge-fill { height: 100%; width: 0%; transition: width 0.1s ease; }

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
        <div class="live-tag">LIVE CAN BUS</div>
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

    <!-- PEDALEIRA FÍSICA -->
    <div class="pedal-box">
        <div class="pedal-unit">
            <div class="pedal-header"><span style="color:var(--red);">[ FREIO / REGEN ]</span><span id="brake-pct-txt" style="color:var(--red);">0.0%</span></div>
            <div class="pedal-stage">
                <div id="pedal-brake" class="pedal-plate brake-plate"><div class="pedal-grip"></div><div class="pedal-grip"></div><div class="pedal-grip"></div></div>
            </div>
            <div class="pedal-gauge"><div id="brake-gauge" class="pedal-gauge-fill" style="background:var(--red);"></div></div>
        </div>
        <div class="pedal-unit">
            <div class="pedal-header"><span style="color:var(--green);">[ ACELERADOR ]</span><span id="throttle-pct-txt" style="color:var(--green);">0.0%</span></div>
            <div class="pedal-stage">
                <div id="pedal-throttle" class="pedal-plate throttle-plate"><div class="pedal-grip"></div><div class="pedal-grip"></div><div class="pedal-grip"></div></div>
            </div>
            <div class="pedal-gauge"><div id="throttle-gauge" class="pedal-gauge-fill" style="background:var(--green);"></div></div>
        </div>
    </div>

    <!-- TABELA CAN -->
    <table>
        <thead><tr><th>s</th><th>km/h</th><th>Marcha</th><th>Embr</th><th>EM(RPM)</th><th>ICE(RPM)</th><th>TPS</th><th>Freio</th><th>Modo</th></tr></thead>
        <tbody id="table-body"></tbody>
    </table>

    <!-- ESQUEMÁTICO e-DCT INTEGRADO -->
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

            // Reset
            ice.classList.remove('active-ice');
            k0.classList.remove('active-k0');
            em.classList.remove('active-em', 'active-em-regen');
            if (c1Top) c1Top.classList.remove('active-clutch1');
            if (c1Bot) c1Bot.classList.remove('active-clutch1');
            if (c2Top) c2Top.classList.remove('active-clutch2');
            if (c2Bot) c2Bot.classList.remove('active-clutch2');

            // Reset engrenagens
            for (let g = 1; g <= 6; g++) {
                const el = svgDoc.getElementById('gear-' + g);
                if (el) el.style.filter = 'none';
            }

            // Ativação da Clutch 1 ou 2
            if (activeClutch === 'CLUTCH_1') {
                if (c1Top) c1Top.classList.add('active-clutch1');
                if (c1Bot) c1Bot.classList.add('active-clutch1');
            } else if (activeClutch === 'CLUTCH_2') {
                if (c2Top) c2Top.classList.add('active-clutch2');
                if (c2Bot) c2Bot.classList.add('active-clutch2');
            }

            // Realce da engrenagem da marcha ativa
            const activeGearEl = svgDoc.getElementById('gear-' + gear);
            if (activeGearEl) {
                activeGearEl.style.filter = 'drop-shadow(0 0 8px #00d2ff)';
            }

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

        async function fetchTelemetry() {
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
                const clutchColor = activeClutch === 'CLUTCH_1' ? 'var(--red)' : 'var(--green)';
                const clutchElem = document.getElementById('val-clutch');
                clutchElem.innerText = clutchLabel;
                clutchElem.style.color = clutchColor;

                document.getElementById('val-rpm-em').innerText = last.rpm_em || '0';
                document.getElementById('val-rpm-ice').innerText = last.rpm_ice || '0';
                document.getElementById('val-k0-press').innerText = last.k0_press_bar || '0.0';
                document.getElementById('val-range').innerText = last.ev_range_km || '0.0';

                // Pedais
                const throttleVal = parseFloat(last.throttle_pct || '0');
                const brakeVal = parseFloat(last.brake_pct || '0');
                document.getElementById('throttle-pct-txt').innerText = throttleVal.toFixed(1) + '%';
                document.getElementById('brake-pct-txt').innerText = brakeVal.toFixed(1) + '%';
                document.getElementById('throttle-gauge').style.width = throttleVal + '%';
                document.getElementById('brake-gauge').style.width = brakeVal + '%';

                document.getElementById('pedal-throttle').style.transform = `rotateX(${(throttleVal/100)*30}deg)`;
                document.getElementById('pedal-brake').style.transform = `rotateX(${(brakeVal/100)*30}deg)`;

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
                    rowsHtml += `<tr><td>${r.timestamp_s}</td><td>${r.speed_kmh}</td><td>${r.gear}</td><td>${r.active_clutch === 'CLUTCH_1' ? 'C1' : 'C2'}</td><td>${r.rpm_em}</td><td>${r.rpm_ice}</td><td>${r.throttle_pct}%</td><td>${r.brake_pct}%</td><td>${r.modo_propulsao}</td></tr>`;
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
