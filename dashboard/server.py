import http.server
import socketserver
import os
import csv
import json

PORT = 8080
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")
SVG_PATH = os.path.join(ROOT_DIR, "module_1_rag", "knowledge_base", "p2_powertrain_topology.svg")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarleyOS | Automotive Cluster</title>
    <style>
        :root {
            --bg: #07090e; --surface: rgba(18, 24, 38, 0.85); --border: rgba(0, 210, 255, 0.25);
            --cyan: #00d2ff; --green: #00e676; --red: #ff3366; --text: #e6edf3; --text-dim: #8b949e;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); padding: 14px; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 14px; }
        .brand { font-weight: 800; font-size: 1.1rem; color: var(--cyan); }
        .grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 14px; }
        .stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 10px; }
        .stat-title { font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase; }
        .stat-val { font-size: 1.25rem; font-weight: 700; margin-top: 4px; }
        table { width: 100%; border-collapse: collapse; font-size: 0.75rem; margin-top: 14px; }
        th, td { border: 1px solid rgba(255, 255, 255, 0.08); padding: 6px 8px; text-align: left; }
        th { background: rgba(15, 22, 36, 0.9); color: var(--text-dim); text-transform: uppercase; }
        .topology-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 12px; margin-top: 18px; }
        .topology-header { font-size: 0.75rem; color: var(--cyan); font-weight: 700; text-transform: uppercase; margin-bottom: 8px; }
        .topology-container { width: 100%; max-height: 180px; display: flex; justify-content: center; }
    </style>
</head>
<body>
    <div class="header">
        <div class="brand">MarleyOS Cockpit // Trem de Força</div>
        <div id="live-indicator" style="font-size: 0.75rem; color: var(--green);">CLUSTER ONLINE (LIVE)</div>
    </div>
    <div class="grid-stats">
        <div class="stat-card"><div class="stat-title">Tacômetro</div><div class="stat-val" style="color:var(--cyan);"><span id="val-rpm">0</span> <span style="font-size:0.75rem; color:var(--text-dim);">RPM</span></div></div>
        <div class="stat-card"><div class="stat-title">Torque Saída</div><div class="stat-val"><span id="val-torque">0.0</span> <span style="font-size:0.75rem; color:var(--text-dim);">Nm</span></div></div>
        <div class="stat-card"><div class="stat-title">Acelerador</div><div class="stat-val"><span id="val-throttle">0.0</span> <span style="font-size:0.75rem; color:var(--text-dim);">%</span></div></div>
        <div class="stat-card"><div class="stat-title">Modo Operação</div><div class="stat-val" style="font-size:0.85rem; color:var(--green);"><span id="val-mode">NOMINAL</span></div></div>
    </div>
    <table>
        <thead><tr><th>Tempo (s)</th><th>RPM</th><th>Torque (Nm)</th><th>Acel (%)</th><th>Modo</th></tr></thead>
        <tbody id="table-body"></tbody>
    </table>
    <div class="topology-card">
        <div class="topology-header">Topologia Mecânica P2 & Acoplamento K0</div>
        <div class="topology-container">
            {{SVG_DIAGRAM}}
        </div>
    </div>
    <script>
        async function fetchTelemetry() {
            try {
                const res = await fetch('/api/telemetry');
                if (!res.ok) return;
                const data = await res.json();
                if (!data.rows || data.rows.length === 0) return;

                const last = data.rows[data.rows.length - 1];
                document.getElementById('val-rpm').innerText = last.rpm || '0';
                document.getElementById('val-torque').innerText = last.torque_nm || '0.0';
                document.getElementById('val-throttle').innerText = last.throttle_pct || '0.0';
                
                const modeElem = document.getElementById('val-mode');
                modeElem.innerText = last.modo_propulsao || 'NOMINAL';
                if (last.modo_propulsao === 'REGEN_BRAKE') {
                    modeElem.style.color = 'var(--red)';
                } else if (last.modo_propulsao === 'P2_HYBRID_BOOST') {
                    modeElem.style.color = 'var(--cyan)';
                } else {
                    modeElem.style.color = 'var(--green)';
                }

                let rowsHtml = '';
                for (let r of data.rows) {
                    rowsHtml += `<tr><td>${r.timestamp_s}</td><td>${r.rpm}</td><td>${r.torque_nm}</td><td>${r.throttle_pct}</td><td>${r.modo_propulsao}</td></tr>`;
                }
                document.getElementById('table-body').innerHTML = rowsHtml;
            } catch (err) {
                console.error('Falha de sincronizacao CAN:', err);
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

        elif self.path in ("/", "/index.html"):
            svg_diagram = ""
            if os.path.exists(SVG_PATH):
                with open(SVG_PATH, "r", encoding="utf-8") as f:
                    svg_diagram = f.read()

            html = HTML_TEMPLATE.replace("{{SVG_DIAGRAM}}", svg_diagram)

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_error(404, "Arquivo nao encontrado")

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ClusterHandler) as httpd:
        print(f"Servidor ativo em http://localhost:{PORT}")
        httpd.serve_forever()
