import http.server
import socketserver
import os
import csv
import json

PORT = 8080
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")

class ClusterHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            rows = []
            if os.path.exists(CSV_PATH):
                with open(CSV_PATH, "r", encoding="utf-8") as f:
                    rows = list(csv.DictReader(f))

            last_row = rows[-1] if rows else {}
            cur_rpm = last_row.get("rpm", "0")
            cur_torque = last_row.get("torque_nm", "0.0")
            cur_throttle = last_row.get("throttle_pct", "0.0")
            cur_mode = last_row.get("modo_propulsao", "NOMINAL")

            table_rows = "".join(
                f"<tr><td>{r.get('timestamp_s', '')}</td><td>{r.get('rpm', '')}</td><td>{r.get('torque_nm', '')}</td><td>{r.get('throttle_pct', '')}</td><td>{r.get('modo_propulsao', '')}</td></tr>"
                for r in rows
            )

            html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarleyOS | Automotive Cluster</title>
    <style>
        :root {{
            --bg: #07090e; --surface: rgba(18, 24, 38, 0.85); --border: rgba(0, 210, 255, 0.25);
            --cyan: #00d2ff; --green: #00e676; --red: #ff3366; --text: #e6edf3; --text-dim: #8b949e;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); padding: 14px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 14px; }}
        .brand {{ font-weight: 800; font-size: 1.1rem; color: var(--cyan); }}
        .grid-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 14px; }}
        .stat-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 10px; }}
        .stat-title {{ font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase; }}
        .stat-val {{ font-size: 1.25rem; font-weight: 700; margin-top: 4px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.75rem; margin-top: 14px; }}
        th, td {{ border: 1px solid rgba(255, 255, 255, 0.08); padding: 6px 8px; text-align: left; }}
        th {{ background: rgba(15, 22, 36, 0.9); color: var(--text-dim); text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="brand">MarleyOS Cockpit // Trem de Força</div>
        <div style="font-size: 0.75rem; color: var(--green);">CLUSTER ONLINE</div>
    </div>
    <div class="grid-stats">
        <div class="stat-card"><div class="stat-title">Tacômetro</div><div class="stat-val" style="color:var(--cyan);">{cur_rpm} <span style="font-size:0.75rem; color:var(--text-dim);">RPM</span></div></div>
        <div class="stat-card"><div class="stat-title">Torque Saída</div><div class="stat-val">{cur_torque} <span style="font-size:0.75rem; color:var(--text-dim);">Nm</span></div></div>
        <div class="stat-card"><div class="stat-title">Acelerador</div><div class="stat-val">{cur_throttle} <span style="font-size:0.75rem; color:var(--text-dim);">%</span></div></div>
        <div class="stat-card"><div class="stat-title">Modo Operação</div><div class="stat-val" style="font-size:0.85rem; color:var(--green);">{cur_mode}</div></div>
    </div>
    <table>
        <thead><tr><th>Tempo (s)</th><th>RPM</th><th>Torque (Nm)</th><th>Acel (%)</th><th>Modo</th></tr></thead>
        <tbody>{table_rows}</tbody>
    </table>
</body>
</html>"""
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
