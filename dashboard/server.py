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

from module_1_rag.pro_rag_engine import AutomotiveEngineeringAI

kb_path = os.path.join(ROOT_DIR, "module_1_rag", "knowledge_base", "automotive_science_and_standards.txt")
engine = AutomotiveEngineeringAI(kb_path)

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
            prompt = payload.get("prompt", "").strip()

            # Processamento inteligente em linguagem natural
            ans = engine.answer_query(prompt)

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
    <title>MarleyOS | Scientific Engineering Cockpit</title>
    <style>
        :root {{
            --bg: #07090e; --surface: rgba(18, 24, 38, 0.75); --border: rgba(0, 210, 255, 0.2);
            --cyan: #00d2ff; --green: #00ffaa; --red: #ff3366; --text: #e6edf3; --text-dim: #8b949e;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg); color: var(--text); padding: 16px; min-height: 100vh;
        }}
        header {{ display: flex; align-items: center; justify-content: space-between; padding-bottom: 14px; border-bottom: 1px solid var(--border); margin-bottom: 16px; }}
        .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1.15rem; color: var(--cyan); }}
        .pulse-orb {{ width: 10px; height: 10px; border-radius: 50%; background: var(--green); box-shadow: 0 0 10px var(--green); }}
        .grid-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 16px; }}
        .stat-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 12px; }}
        .stat-title {{ font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; font-weight: 600; }}
        .stat-val {{ font-size: 1.35rem; font-weight: 700; color: #fff; margin-top: 4px; }}
        .glass-panel {{ background: var(--surface); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 16px; margin-bottom: 16px; }}
        .panel-header {{ font-size: 0.95rem; font-weight: 700; color: var(--cyan); margin-bottom: 12px; }}
        #chat-window {{ height: 280px; overflow-y: auto; background: rgba(10, 14, 22, 0.9); border-radius: 10px; padding: 14px; border: 1px solid rgba(0, 210, 255, 0.15); font-size: 0.85rem; display: flex; flex-direction: column; gap: 12px; margin-bottom: 10px; }}
        .msg-bubble {{ padding: 10px 14px; border-radius: 10px; max-width: 96%; line-height: 1.5; }}
        .msg-user {{ align-self: flex-end; background: rgba(0, 210, 255, 0.2); border: 1px solid rgba(0, 210, 255, 0.4); color: #fff; }}
        .msg-bot {{ align-self: flex-start; background: rgba(0, 255, 170, 0.08); border: 1px solid rgba(0, 255, 170, 0.25); color: #e1e7ec; }}
        pre {{ background: #05070a; padding: 10px; border-radius: 6px; border: 1px solid #1f2a3a; overflow-x: auto; color: #00d2ff; font-family: monospace; font-size: 0.8rem; margin: 8px 0; }}
        code {{ font-family: monospace; color: #00ffaa; }}
        .input-box {{ display: flex; gap: 8px; }}
        input {{ flex: 1; padding: 12px 14px; background: rgba(12, 17, 28, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); color: #fff; border-radius: 8px; outline: none; font-size: 0.85rem; }}
        button {{ padding: 12px 20px; background: linear-gradient(135deg, #00d2ff 0%, #0072ff 100%); border: none; border-radius: 8px; color: #fff; font-weight: 700; cursor: pointer; }}
        .table-wrap {{ overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.78rem; }}
        th {{ background: rgba(15, 22, 36, 0.9); color: var(--text-dim); text-transform: uppercase; font-size: 0.7rem; padding: 8px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }}
        .badge-time {{ background: rgba(255, 255, 255, 0.08); padding: 2px 6px; border-radius: 4px; font-family: monospace; }}
        .status-pill {{ padding: 3px 8px; border-radius: 20px; font-weight: 700; font-size: 0.7rem; }}
        .status-pill.ok {{ background: rgba(0, 255, 170, 0.15); color: var(--green); }}
        .status-pill.crit-pulse {{ background: rgba(255, 51, 102, 0.2); color: var(--red); }}
    </style>
</head>
<body>
    <header>
        <div class="brand">🔬 MarleyOS | Expert Systems Engineering</div>
        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: var(--text-dim);">
            <div class="pulse-orb"></div> RAG CIENTÍFICO ATIVO
        </div>
    </header>

    <div class="grid-stats">
        <div class="stat-card"><div class="stat-title">🏎️ Rotação</div><div class="stat-val">{cur_rpm} <span style="font-size:0.75rem; color:var(--text-dim);">RPM</span></div></div>
        <div class="stat-card"><div class="stat-title">⚡ Carga Pack</div><div class="stat-val">{cur_curr} <span style="font-size:0.75rem; color:var(--text-dim);">A</span></div></div>
        <div class="stat-card"><div class="stat-title">🛡️ Isolamento</div><div class="stat-val">{cur_iso} <span style="font-size:0.75rem; color:var(--text-dim);">kΩ</span></div></div>
        <div class="stat-card"><div class="stat-title">⚠️ Status Global</div><div class="stat-val" style="font-size:0.85rem; color: {'var(--red)' if is_alert else 'var(--green)'};">{cur_stat}</div></div>
    </div>

    <div class="glass-panel">
        <div class="panel-header">Copilot de Engenharia & Consultoria Científica</div>
        <div id="chat-window">
            <div class="msg-bubble msg-bot">
                <b>Copilot:</b> Conectado ao acervo técnico: <b>UN ECE R100, ISO 26262 e MathWorks Agent Skills</b>[span_4](start_span)[span_4](end_span).<br>
                Experimente: <i>'Como montar um modelo Simulink moderno?'</i> ou <i>'Explique os requisitos de isolamento para alta tensão'</i>[span_5](start_span)[span_5](end_span).
            </div>
        </div>
        <div class="input-box">
            <input id="prompt-input" type="text" placeholder="Tire dúvidas científicas ou solicite um modelo de simulação..." onkeydown="if(event.key==='Enter') send()">
            <button onclick="send()">Consultar</button>
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
        function formatMarkdown(text) {{
            return text
                .replace(/```matlab([\\s\\S]*?)```/g, '<pre><code>$1</code></pre>')
                .replace(/```([\\s\\S]*?)```/g, '<pre><code>$1</code></pre>')
                .replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>')
                .replace(/\\*(.*?)\\*/g, '<i>$1</i>')
                .replace(/\\n/g, '<br>');
        }}

        async function send() {{
            const input = document.getElementById('prompt-input');
            const text = input.value.trim();
            if(!text) return;
            const win = document.getElementById('chat-window');
            win.innerHTML += `<div class="msg-bubble msg-user"><b>Engenheiro:</b> ${{text}}</div>`;
            input.value = '';
            win.scrollTop = win.scrollHeight;

            try {{
                const res = await fetch('/api/chat', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{prompt: text}})
                }});
                const data = await res.json();
                win.innerHTML += `<div class="msg-bubble msg-bot">${{formatMarkdown(data.reply)}}</div>`;
            }} catch(e) {{
                win.innerHTML += `<div class="msg-bubble msg-bot" style="color:var(--red);">Erro no pipeline semântico.</div>`;
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
    print(f"[+] Scientific Cockpit ativo em http://localhost:{PORT}")
    with ReusableTCPServer(("", PORT), DashboardHandler) as httpd:
        httpd.serve_forever()
