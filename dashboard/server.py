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
                ans = f"Telemetria CAN: Corrente {s.get('corrente_max_a')} A | Temp {s.get('temp_max_c')} °C | RPM {s.get('rpm_max')}."
            elif any(k in prompt for k in ["freio", "abs", "c0035"]):
                docs = load_documents()
                res = retrieve("C0035", docs, k=1)
                ans = f"Diagnostico ABS (RAG): {res[0]}" if res else "Sem dados de freios."
            elif any(k in prompt for k in ["direcao", "eps", "c1555"]):
                docs = load_documents()
                res = retrieve("C1555", docs, k=1)
                ans = f"Diagnostico EPS (RAG): {res[0]}" if res else "Sem dados de direcao."
            elif any(k in prompt for k in ["iso", "asil", "seguranca"]):
                ans = evaluate_functional_safety("Falha: C0035 Falha no sensor de velocidade da roda com frenagem regenerativa ativa.")
            else:
                ans = "Copilot Automotivo: Consulte sobre 'telemetria', 'freio ABS (C0035)', 'direção EPS (C1555)' ou 'segurança ISO'."

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
                f"<tr><td>{r.get('timestamp_s')}</td><td>{r.get('rpm_motor')}</td><td>{r.get('corrente_pack_a')} A</td><td>{r.get('pressao_freio_bar')} bar</td><td>{r.get('torque_eps_nm')} Nm</td><td style='color:{'#ff4d4d' if r.get('status_falha')!='NORMAL' else '#00ff88'}'>{r.get('status_falha')}</td></tr>"
                for r in rows
            ])

            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarleyOS - Multi-Component Copilot</title>
    <style>
        body {{ font-family: monospace; background: #0b0f17; color: #d1d7e0; margin: 0; padding: 15px; }}
        h2 {{ color: #00d2ff; }}
        .card {{ background: #161c26; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #232d3d; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 11px; }}
        th, td {{ border: 1px solid #2a3649; padding: 5px; text-align: left; }}
        th {{ background: #1e2837; }}
        #chat-window {{ height: 180px; overflow-y: auto; background: #0d121a; padding: 10px; border-radius: 6px; border: 1px solid #232d3d; font-size: 12px; margin-bottom: 10px; }}
        .msg-user {{ color: #00d2ff; margin-bottom: 6px; }}
        .msg-bot {{ color: #38ef7d; margin-bottom: 10px; }}
        .input-row {{ display: flex; gap: 8px; }}
        input {{ flex: 1; padding: 10px; background: #121822; border: 1px solid #2a3649; color: #fff; border-radius: 4px; font-family: monospace; }}
        button {{ padding: 10px 16px; background: #00d2ff; color: #0b0f17; border: none; font-weight: bold; border-radius: 4px; cursor: pointer; }}
    </style>
</head>
<body>
    <h2>MarleyOS | Sistema Multi-Componente (Inversor + Freio + EPS)</h2>
    <div class="card">
        <strong>Copilot de Engenharia Automotiva</strong>
        <div id="chat-window">
            <div class="msg-bot"><b>Copilot:</b> Monitorando Inversor de Tração, Freio Regenerativo (ABS) e Direção Elétrica (EPS). Envie sua pergunta.</div>
        </div>
        <div class="input-row">
            <input id="prompt-input" type="text" placeholder="Ex: Procedimento para falha no freio ABS?" onkeydown="if(event.key==='Enter') send()">
            <button onclick="send()">Enviar</button>
        </div>
    </div>
    <div class="card">
        <strong>Telemetria CAN Completa</strong>
        <table>
            <tr><th>Tempo</th><th>RPM</th><th>Corrente</th><th>Freio</th><th>EPS</th><th>Status</th></tr>
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
    print(f"[+] Multi-Component Dashboard ativo em http://localhost:{PORT}")
    with ReusableTCPServer(("", PORT), DashboardHandler) as httpd:
        httpd.serve_forever()
