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
                ans = f"⚡ Telemetria Ativa: Corrente Max {s.get('corrente_max_a')} A | Temp Max {s.get('temp_max_c')} °C | RPM {s.get('rpm_max')}."
            elif any(k in prompt for k in ["bpcm", "isolamento", "p0aa6"]):
                docs = load_documents()
                res = retrieve("P0AA6", docs, k=1)
                ans = f"🔋 BPCM Diagnostic: {res[0]}" if res else "Sem informações do BPCM."
            elif any(k in prompt for k in ["ecm", "p0606"]):
                docs = load_documents()
                res = retrieve("P0606", docs, k=1)
                ans = f"⚙️ ECM Powertrain: {res[0]}" if res else "Sem dados do ECM."
            elif any(k in prompt for k in ["tcm", "p0700"]):
                docs = load_documents()
                res = retrieve("P0700", docs, k=1)
                ans = f"🕹️ TCM Transmission: {res[0]}" if res else "Sem dados do TCM."
            elif any(k in prompt for k in ["bcm", "b1000"]):
                docs = load_documents()
                res = retrieve("B1000", docs, k=1)
                ans = f"💡 BCM Body: {res[0]}" if res else "Sem dados do BCM."
            elif any(k in prompt for k in ["freio", "abs", "c0035"]):
                docs = load_documents()
                res = retrieve("C0035", docs, k=1)
                ans = f"🛑 ABS Brake: {res[0]}" if res else "Sem dados de freios."
            elif any(k in prompt for k in ["direcao", "eps", "c1555"]):
                docs = load_documents()
                res = retrieve("C1555", docs, k=1)
                ans = f"🎯 EPS Steering: {res[0]}" if res else "Sem dados de direção."
            elif any(k in prompt for k in ["iso", "asil", "seguranca"]):
                ans = evaluate_functional_safety("Falha: P0AA6 Perda de isolamento no pack de alta tensao monitorado pelo BPCM.")
            else:
                ans = "🤖 Copilot: Consulte sobre 'ECM', 'BPCM', 'TCM', 'BCM', 'ABS', 'EPS' ou 'ISO 26262'."

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

            # Métricas dinâmicas do topo
            last_row = rows[-1] if rows else {}
            cur_rpm = last_row.get("rpm_motor", "0")
            cur_curr = last_row.get("corrente_pack_a", "0.0")
            cur_iso = last_row.get("bpcm_isolamento_kohm", "500")
            cur_stat = last_row.get("status_falha", "NORMAL")
            is_alert = cur_stat != "NORMAL"

            table_rows = "".join([
                f"""<tr>
                    <td><span class='badge-time'>{r.get('timestamp_s')}s</span></td>
                    <td><b>{r.get('rpm_motor')}</b></td>
                    <td>{r.get('corrente_pack_a')} A</td>
                    <td>{r.get('bcm_tensao_v')} V</td>
                    <td>{r.get('tcm_pressao_bar')} bar</td>
                    <td>{r.get('bpcm_isolamento_kohm')} kΩ</td>
                    <td><span class='{'status-pill crit-pulse' if r.get('status_falha')!='NORMAL' else 'status-pill ok'}'>{r.get('status_falha')}</span></td>
                </tr>"""
                for r in rows
            ])

            html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarleyOS | Next-Gen AI Cockpit</title>
    <style>
        :root {{
            --bg: #07090e;
            --surface: rgba(18, 24, 38, 0.7);
            --border: rgba(0, 210, 255, 0.2);
            --cyan: #00d2ff;
            --green: #00ffaa;
            --red: #ff3366;
            --text: #e6edf3;
            --text-dim: #8b949e;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            background-image: radial-gradient(circle at 10% 20%, rgba(0, 210, 255, 0.08) 0%, transparent 40%),
                              radial-gradient(circle at 90% 80%, rgba(255, 51, 102, 0.08) 0%, transparent 40%);
            color: var(--text);
            padding: 16px;
            min-height: 100vh;
        }}
        header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 16px;
        }}
        .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1.2rem; color: var(--cyan); }}
        .pulse-orb {{
            width: 12px; height: 12px; border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 12px var(--green);
            animation: orb 1.8s infinite ease-in-out;
        }}
        @keyframes orb {{ 0%, 100% {{ opacity: 0.4; transform: scale(0.9); }} 50% {{ opacity: 1; transform: scale(1.2); }} }}

        /* Métricas Rápidas */
        .grid-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 10px;
            margin-bottom: 16px;
        }}
        .stat-card {{
            background: var(--surface);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 12px;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s ease;
        }}
        .stat-card:hover {{ transform: translateY(-2px); }}
        .stat-title {{ font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; font-weight: 600; display: flex; align-items: center; gap: 4px; }}
        .stat-val {{ font-size: 1.4rem; font-weight: 700; color: #fff; margin-top: 6px; }}
        .stat-card::after {{
            content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, var(--cyan), transparent);
        }}

        /* Seções / Cards */
        .glass-panel {{
            background: var(--surface);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }}
        .panel-header {{
            font-size: 0.95rem; font-weight: 700; color: var(--cyan);
            margin-bottom: 12px; display: flex; align-items: center; gap: 8px;
        }}

        /* Chat Moderno */
        #chat-window {{
            height: 200px;
            overflow-y: auto;
            background: rgba(10, 14, 22, 0.85);
            border-radius: 10px;
            padding: 12px;
            border: 1px solid rgba(0, 210, 255, 0.15);
            font-size: 0.85rem;
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 10px;
        }}
        .msg-bubble {{
            padding: 8px 12px; border-radius: 10px; max-width: 88%; line-height: 1.4;
            animation: fadeIn 0.2s ease-in-out;
        }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .msg-user {{
            align-self: flex-end; background: rgba(0, 210, 255, 0.18);
            border: 1px solid rgba(0, 210, 255, 0.3); color: #fff;
        }}
        .msg-bot {{
            align-self: flex-start; background: rgba(0, 255, 170, 0.08);
            border: 1px solid rgba(0, 255, 170, 0.25); color: #e1e7ec;
        }}
        .input-box {{ display: flex; gap: 8px; }}
        input {{
            flex: 1; padding: 12px 14px; background: rgba(12, 17, 28, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.15); color: #fff;
            border-radius: 8px; outline: none; font-size: 0.85rem;
            transition: border-color 0.2s;
        }}
        input:focus {{ border-color: var(--cyan); box-shadow: 0 0 8px rgba(0, 210, 255, 0.3); }}
        button {{
            padding: 12px 18px;
            background: linear-gradient(135deg, #00d2ff 0%, #0072ff 100%);
            border: none; border-radius: 8px; color: #fff; font-weight: 700;
            cursor: pointer; display: flex; align-items: center; gap: 6px;
            box-shadow: 0 4px 15px rgba(0, 210, 255, 0.25);
            transition: transform 0.1s ease;
        }}
        button:active {{ transform: scale(0.96); }}

        /* Tabela Estilizada */
        .table-wrap {{ overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.78rem; }}
        th {{
            background: rgba(15, 22, 36, 0.9);
            color: var(--text-dim); text-transform: uppercase; font-size: 0.7rem;
            padding: 10px 8px; text-align: left; border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        td {{ padding: 10px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }}
        .badge-time {{
            background: rgba(255, 255, 255, 0.08); padding: 2px 6px;
            border-radius: 4px; font-family: monospace;
        }}
        .status-pill {{
            padding: 3px 8px; border-radius: 20px; font-weight: 700; font-size: 0.7rem;
            display: inline-block; text-align: center;
        }}
        .status-pill.ok {{ background: rgba(0, 255, 170, 0.15); color: var(--green); border: 1px solid rgba(0, 255, 170, 0.3); }}
        .status-pill.crit-pulse {{
            background: rgba(255, 51, 102, 0.2); color: var(--red);
            border: 1px solid rgba(255, 51, 102, 0.5);
            animation: blink 1.2s infinite ease-in-out;
        }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
            MarleyOS Cockpit
        </div>
        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: var(--text-dim);">
            <div class="pulse-orb"></div> MCP BUS ATIVO
        </div>
    </header>

    <!-- Indicadores no Topo -->
    <div class="grid-stats">
        <div class="stat-card">
            <div class="stat-title">🏎️ Rotação</div>
            <div class="stat-val">{cur_rpm} <span style="font-size:0.75rem; color:var(--text-dim);">RPM</span></div>
        </div>
        <div class="stat-card">
            <div class="stat-title">⚡ Carga Pack</div>
            <div class="stat-val">{cur_curr} <span style="font-size:0.75rem; color:var(--text-dim);">A</span></div>
        </div>
        <div class="stat-card">
            <div class="stat-title">🛡️ Isolamento</div>
            <div class="stat-val">{cur_iso} <span style="font-size:0.75rem; color:var(--text-dim);">kΩ</span></div>
        </div>
        <div class="stat-card">
            <div class="stat-title">⚠️ Status Global</div>
            <div class="stat-val" style="font-size:0.9rem; color: {'var(--red)' if is_alert else 'var(--green)'};">{cur_stat}</div>
        </div>
    </div>

    <!-- Terminal de Chat com Agente de IA -->
    <div class="glass-panel">
        <div class="panel-header">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            Copilot de Engenharia Automotiva
        </div>
        <div id="chat-window">
            <div class="msg-bubble msg-bot">
                <b>Copilot:</b> Hub de telemetria inicializado. Monitorando <b>ECM, BCM, TCM, BPCM, ABS e EPS</b> via protocolo MCP. O que deseja auditar?
            </div>
        </div>
        <div class="input-box">
            <input id="prompt-input" type="text" placeholder="Pergunte sobre falha de isolamento P0AA6 ou status do ECM..." onkeydown="if(event.key==='Enter') send()">
            <button onclick="send()">
                Enviar
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
                </svg>
            </button>
        </div>
    </div>

    <!-- Telemetria do Barramento CAN -->
    <div class="glass-panel">
        <div class="panel-header">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
            </svg>
            Telemetria Integrada de Bordo (Multi-ECU CAN Bus)
        </div>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr><th>Tempo</th><th>RPM</th><th>Corrente</th><th>BCM</th><th>TCM</th><th>BPCM</th><th>Status</th></tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        async function send() {{
            const input = document.getElementById('prompt-input');
            const text = input.value.trim();
            if(!text) return;
            const win = document.getElementById('chat-window');
            win.innerHTML += `<div class="msg-bubble msg-user"><b>Você:</b> ${{text}}</div>`;
            input.value = '';
            win.scrollTop = win.scrollHeight;

            try {{
                const res = await fetch('/api/chat', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{prompt: text}})
                }});
                const data = await res.json();
                win.innerHTML += `<div class="msg-bubble msg-bot"><b>Copilot:</b> ${{data.reply}}</div>`;
            }} catch(e) {{
                win.innerHTML += `<div class="msg-bubble msg-bot" style="color:var(--red);">Erro de comunicação com o backend MCP.</div>`;
            }}
            win.scrollTop = win.scrollHeight;
        }}
    </script>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()

if __name__ == "__main__":
    print(f"[+] Modern Cockpit ativo em http://localhost:{PORT}")
    with ReusableTCPServer(("", PORT), DashboardHandler) as httpd:
        httpd.serve_forever()
