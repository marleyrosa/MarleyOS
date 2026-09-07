import http.server
import socketserver
import json
import os
import csv
import sys

PORT = 8080
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from module_1_rag.rag_engine import load_documents, retrieve
from module_2_mcp.mcp_server import handle_rpc
from module_4_finetuning.iso_safety_validator import evaluate_functional_safety

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/chat":
            length = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length).decode('utf-8')) if length else {}
            prompt = payload.get("prompt", "").lower()

            if any(k in prompt for k in ["corrente", "pico", "telemetria", "status"]):
                s = handle_rpc({"method": "tools/call", "params": {"name": "get_telemetry_summary"}})
                ans = f"Pico de corrente registrado: {s.get('corrente_max_a')} A | Temperatura pico: {s.get('temp_max_c')} °C | RPM max: {s.get('rpm_max')}."
            elif any(k in prompt for k in ["falha", "critico", "alarme"]):
                c = handle_rpc({"method": "tools/call", "params": {"name": "get_critical_events"}}).get("eventos_criticos", [])
                ans = f"Eventos criticos encontrados ({len(c)}): " + ", ".join([e.get("status_falha", "") for e in c])
            elif any(k in prompt for k in ["p0a80", "bateria", "manual"]):
                docs = load_documents()
                res = retrieve(prompt, docs, k=1)
                ans = f"Base RAG: {res[0]}" if res else "Sem dados tecnicos catalogados."
            elif any(k in prompt for k in ["iso", "asil", "seguranca"]):
                ans = evaluate_functional_safety("Falha: Corrente do pack atingiu 315A excedendo limiar de 300A.")
            else:
                ans = "Comando nao reconhecido. Consulte 'telemetria', 'alarmes', 'ISO 26262' ou 'P0A80'."

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"reply": ans}).encode('utf-8'))

    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            telemetry_path = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")
            rows = []
            if os.path.exists(telemetry_path):
                with open(telemetry_path, 'r', encoding='utf-8') as f:
                    rows = list(csv.DictReader(f))

            table_rows = "".join([
                f"<tr><td>{r.get('timestamp_s')}</td><td>{r.get('rpm_motor')}</td><td>{r.get('corrente_pack_a')} A</td><td>{r.get('temp_inversor_c')} °C</td><td style='color:{'#ff4d4d' if r.get('status_falha')!='NORMAL' else '#00ff88'}'>{r.get('status_falha')}</td></tr>"
                for r in rows
            ])

            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarleyOS - Copilot Automotivo</title>
    <style>
        body {{ font-family: monospace; background: #0b0f17; color: #d1d7e0; margin: 0; padding: 15px; }}
        h2 {{ color: #00d2ff; margin-bottom: 8px; }}
        .card {{ background: #161c26; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #232d3d; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
        th, td {{ border: 1px solid #2a3649; padding: 6px; text-align: left; }}
        th {{ background: #1e2837; }}
        #chat-window {{ height: 180px; overflow-y: auto; background: #0d121a; padding: 10px; border-radius: 6px; border: 1px solid #232d3d; font-size: 13px; margin-bottom: 10px; }}
        .msg-user {{ color: #00d2ff; margin-bottom: 6px; }}
        .msg-bot {{ color: #38ef7d; margin-bottom: 10px; }}
        .input-row {{ display: flex; gap: 8px; }}
        input {{ flex: 1; padding: 10px; background: #121822; border: 1px solid #2a3649; color: #fff; border-radius: 4px; font-family: monospace; }}
        button {{ padding: 10px 16px; background: #00d2ff; color: #0b0f17; border: none; font-weight: bold; border-radius: 4px; cursor: pointer; }}
    </style>
</head>
<body>
    <h2>MarleyOS | Automotive AI Copilot</h2>

    <div class="card">
        <strong>Terminal de Chat com a IA</strong>
        <div id="chat-window">
            <div class="msg-bot"><b>Copilot:</b> Telemetria CAN conectada via MCP. Pode consultar os parametros ou normas de seguranca.</div>
        </div>
        <div class="input-row">
            <input id="prompt-input" type="text" placeholder="Ex: Qual o pico de corrente da telemetria?" onkeydown="if(event.key==='Enter') send()">
            <button onclick="send()">Enviar</button>
        </div>
    </div>

    <div class="card">
        <strong>Telemetria de Rodagem (CAN Bus - MCP)</strong>
        <table>
            <tr><th>Tempo</th><th>RPM</th><th>Corrente</th><th>Temp</th><th>Status</th></tr>
            {table_rows}
        </table>
    </div>

    <script>
        async function send() {{
            const input = document.getElementById('prompt-input');
            const text = input.value.trim();
            if(!text) return;
            const win = document.getElementById('chat-window');
            win.innerHTML += `<div class="msg-user"><b>Voce:</b> ${{text}}</div>`;
            input.value = '';
            win.scrollTop = win.scrollHeight;

            const res = await fetch('/api/chat', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{prompt: text}})
            }});
            const data = await res.json();
            win.innerHTML += `<div class="msg-bot"><b>Copilot:</b> ${{data.reply}}</div>`;
            win.scrollTop = win.scrollHeight;
        }}
    </script>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()

if __name__ == "__main__":
    print(f"[+] Interface Interativa rodando em http://localhost:{PORT}")
    with ReusableTCPServer(("", PORT), DashboardHandler) as httpd:
        httpd.serve_forever()
