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
from skills.mathworks_agent_skill import SimulinkAgentSkill

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def finish(self):
        try:
            if not self.wfile.closed:
                self.wfile.flush()
            super().finish()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_POST(self):
        if self.path == "/api/chat":
            length = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length).decode('utf-8')) if length else {}
            prompt = payload.get("prompt", "").lower()

            # Rota pedagógica / Skills da MathWorks
            if any(k in prompt for k in ["aprender", "explicar", "conceito", "skill"]):
                if "simulink" in prompt or "simulation" in prompt:
                    ans = "🎓 [Learning Skill]: " + SimulinkAgentSkill.explain_concept("simulation_input")
                elif "asil" in prompt or "segurança" in prompt:
                    ans = "🎓 [Learning Skill]: " + SimulinkAgentSkill.explain_concept("asil_d")
                elif "bpcm" in prompt or "isolamento" in prompt:
                    ans = "🎓 [Learning Skill]: " + SimulinkAgentSkill.explain_concept("bpcm_isolation")
                else:
                    ans = "🎓 [Learning Skill]: Posso explicar sobre 'Simulink SimulationInput', 'ASIL-D' ou 'Isolamento do BPCM'."
            elif any(k in prompt for k in ["corrente", "pico", "telemetria", "status"]):
                s = handle_rpc({"method": "tools/call", "params": {"name": "get_telemetry_summary"}})
                ans = f"⚡ Telemetria Ativa: Corrente {s.get('corrente_max_a')} A | Temp {s.get('temp_max_c')} °C | RPM {s.get('rpm_max')}."
            elif any(k in prompt for k in ["bpcm", "isolamento", "p0aa6"]):
                docs = load_documents()
                res = retrieve("P0AA6", docs, k=1)
                ans = f"🔋 BPCM Diagnostic: {res[0]}" if res else "Sem informações do BPCM."
            elif any(k in prompt for k in ["ecm", "p0606"]):
                docs = load_documents()
                res = retrieve("P0606", docs, k=1)
                ans = f"⚙️ ECM Powertrain: {res[0]}" if res else "Sem dados do ECM."
            elif any(k in prompt for k in ["iso", "asil", "seguranca"]):
                ans = evaluate_functional_safety("Falha: P0AA6 Perda de isolamento no pack de alta tensao monitorado pelo BPCM.")
            else:
                ans = "🤖 Copilot: Consulte sobre falhas (P0AA6, P0606), telemetria ou use 'Explicar conceito de Simulink' para aprender."

            body = json.dumps({"reply": ans}).encode('utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            telemetry_path = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")
            rows = []
            if os.path.exists(telemetry_path):
                with open(telemetry_path, 'r', encoding='utf-8') as f:
                    rows = list(csv.DictReader(f))

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

            html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarleyOS | Learning & AI Cockpit</title>
    <style>
        :root {{
            --bg: #07090e; --surface: rgba(18, 24, 38, 0.7); --border: rgba(0, 210, 255, 0.2);
            --cyan: #00d2ff; --green: #00ffaa; --red: #ff3366; --text: #e6edf3; --text-dim: #8b949e;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            background-image: radial-gradient(circle at 10% 20%, rgba(0, 210, 255, 0.08) 0%, transparent 40%),
                              radial-gradient(circle at 90% 80%, rgba(255, 51, 102, 0.08) 0%, transparent 40%);
            color: var(--text); padding: 16px; min-height: 100vh;
        }}
        header {{ display: flex; align-items: center; justify-content: space-between; padding-bottom: 16px; border-bottom: 1px solid var(--border); margin-bottom: 16px; }}
        .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1.2rem; color: var(--cyan); }}
        .pulse-orb {{ width: 12px; height: 12px; border-radius: 50%; background: var(--green); box-shadow: 0 0 12px var(--green); }}
        .grid-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 16px; }}
        .stat-card {{ background: var(--surface); backdrop-filter: blur(12px); border: 1px solid var(--border); border-radius: 12px; padding: 12px; position: relative; }}
        .stat-title {{ font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; font-weight: 600; }}
        .stat-val {{ font-size: 1.4rem; font-weight: 700; color: #fff; margin-top: 6px; }}
        .glass-panel {{ background: var(--surface); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 16px; margin-bottom: 16px; }}
        .panel-header {{ font-size: 0.95rem; font-weight: 700; color: var(--cyan); margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
        #chat-window {{ height: 200px; overflow-y: auto; background: rgba(10, 14, 22, 0.85); border-radius: 10px; padding: 12px; border: 1px solid rgba(0, 210, 255, 0.15); font-size: 0.85rem; display: flex; flex-direction: column; gap: 10px; margin-bottom: 10px; }}
        .msg-bubble {{ padding: 8px 12px; border-radius: 10px; max-width: 88%; line-height: 1.4; }}
        .msg-user {{ align-self: flex-end; background: rgba(0, 210, 255, 0.18); border: 1px solid rgba(0, 210, 255, 0.3); color: #fff; }}
        .msg-bot {{ align-self: flex-start; background: rgba(0, 255, 170, 0.08); border: 1px solid rgba(0, 255, 170, 0.25); color: #e1e7ec; }}
        .input-box {{ display: flex; gap: 8px; }}
        input {{ flex: 1; padding: 12px 14px; background: rgba(12, 17, 28, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); color: #fff; border-radius: 8px; outline: none; }}
        button {{ padding: 12px 18px; background: linear-gradient(135deg, #00d2ff 0%, #0072ff 100%); border: none; border-radius: 8px; color: #fff; font-weight: 700; cursor: pointer; }}
        .table-wrap {{ overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.78rem; }}
        th {{ background: rgba(15, 22, 36, 0.9); color: var(--text-dim); text-transform: uppercase; font-size: 0.7rem; padding: 10px 8px; text-align: left; }}
        td {{ padding: 10px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }}
        .badge-time {{ background: rgba(255, 255, 255, 0.08); padding: 2px 6px; border-radius: 4px; font-family: monospace; }}
        .status-pill {{ padding: 3px 8px; border-radius: 20px; font-weight: 700; font-size: 0.7rem; display: inline-block; }}
        .status-pill.ok {{ background: rgba(0, 255, 170, 0.15); color: var(--green); }}
        .status-pill.crit-pulse {{ background: rgba(255, 51, 102, 0.2); color: var(--red); }}
    </style>
</head>
<body>
    <header>
        <div class="brand">MarleyOS AI Learning Cockpit</div>
        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: var(--text-dim);">
            <div class="pulse-orb"></div> MCP & SKILLS ATIVAS
        </div>
    </header>
    <div class="grid-stats">
        <div class="stat-card"><div class="stat-title">🏎️ Rotação</div><div class="stat-val">{cur_rpm} <span style="font-size:0.75rem; color:var(--text-dim);">RPM</span></div></div>
        <div class="stat-card"><div class="stat-title">⚡ Carga Pack</div><div class="stat-val">{cur_curr} <span style="font-size:0.75rem; color:var(--text-dim);">A</span></div></div>
        <div class="stat-card"><div class="stat-title">🛡️ Isolamento</div><div class="stat-val">{cur_iso} <span style="font-size:0.75rem; color:var(--text-dim);">kΩ</span></div></div>
        <div class="stat-card"><div class="stat-title">⚠️ Status Global</div><div class="stat-val" style="font-size:0.9rem; color: {'var(--red)' if is_alert else 'var(--green)'};">{cur_stat}</div></div>
    </div>
    <div class="glass-panel">
        <div class="panel-header">Copilot de Engenharia & Tutoria Inteligente</div>
        <div id="chat-window">
            <div class="msg-bubble msg-bot"><b>Copilot:</b> Olá! Além de monitorar telemetria e normas ISO, agora conto com <b>MathWorks Agent Skills</b>. Pergunte: <i>'Explicar conceito de Simulink'</i> ou <i>'O que significa ASIL-D?'</i>.</div>
        </div>
        <div class="input-box">
            <input id="prompt-input" type="text" placeholder="Pergunte sobre telemetria ou peça uma explicação de conceito..." onkeydown="if(event.key==='Enter') send()">
            <button onclick="send()">Enviar</button>
        </div>
    </div>
    <div class="glass-panel">
        <div class="panel-header">Telemetria de Bancada Integrada (CAN Bus)</div>
        <div class="table-wrap">
            <table>
                <thead><tr><th>Tempo</th><th>RPM</th><th>Corrente</th><th>BCM</th><th>TCM</th><th>BPCM</th><th>Status</th></tr></thead>
                <tbody>{table_rows}</tbody>
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
                win.innerHTML += `<div class="msg-bubble msg-bot" style="color:var(--red);">Erro no socket MCP.</div>`;
            }}
            win.scrollTop = win.scrollHeight;
        }}
    </script>
</body>
</html>"""
            body = html_content.encode('utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass
        else:
            super().do_GET()

if __name__ == "__main__":
    print(f"[+] Cockpit de Aprendizagem ativo em http://localhost:{PORT}")
    with ReusableTCPServer(("", PORT), DashboardHandler) as httpd:
        httpd.serve_forever()
