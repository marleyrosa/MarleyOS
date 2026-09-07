import http.server
import socketserver
import os
import csv

PORT = 8080
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            # Carregar telemetria
            telemetry_path = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")
            rows = []
            if os.path.exists(telemetry_path):
                with open(telemetry_path, 'r', encoding='utf-8') as f:
                    rows = list(csv.DictReader(f))
                    
            # Carregar parecer Capstone
            report_path = os.path.join(ROOT_DIR, "module_6_capstone_project", "capstone_report.txt")
            report_txt = "Nenhum relatório emitido."
            if os.path.exists(report_path):
                with open(report_path, 'r', encoding='utf-8') as f:
                    report_txt = f.read()

            table_rows = "".join([
                f"<tr><td>{r.get('timestamp_s')}</td><td>{r.get('rpm_motor')}</td><td>{r.get('corrente_pack_a')} A</td><td>{r.get('temp_inversor_c')} °C</td><td style='color:{'#ff4d4d' if r.get('status_falha')!='NORMAL' else '#00ff88'}'>{r.get('status_falha')}</td></tr>"
                for r in rows
            ])

            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>MarleyOS - Automotive AI Dashboard</title>
    <style>
        body {{ font-family: monospace; background: #0f141c; color: #e1e7ec; padding: 20px; }}
        h1 {{ color: #00d2ff; }}
        .card {{ background: #1b222d; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #00d2ff; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ border: 1px solid #2d3848; padding: 8px; text-align: left; }}
        th {{ background: #242e3e; }}
        pre {{ background: #121820; padding: 12px; border-radius: 6px; overflow-x: auto; color: #38ef7d; }}
    </style>
</head>
<body>
    <h1>MarleyOS | Painel de Telemetria & IA Automotiva</h1>
    <div class="card">
        <h3>Dados de Rodagem (Barramento CAN - MCP)</h3>
        <table>
            <tr><th>Tempo (s)</th><th>RPM</th><th>Corrente</th><th>Temp Inversor</th><th>Status</th></tr>
            {table_rows}
        </table>
    </div>
    <div class="card">
        <h3>Último Parecer de Segurança Funcional (ISO 26262 / ASIL)</h3>
        <pre>{report_txt}</pre>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()

if __name__ == "__main__":
    print(f"[+] Dashboard ativo. Acesse no navegador: http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        httpd.serve_forever()
