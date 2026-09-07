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

from module_1_rag.pro_rag_engine import ProfessionalAutomotiveRAG

json_kb = os.path.join(ROOT_DIR, "module_1_rag", "knowledge_base", "simulink_systems.json")
std_kb = os.path.join(ROOT_DIR, "module_1_rag", "knowledge_base", "automotive_science_and_standards.txt")
engine = ProfessionalAutomotiveRAG(json_kb, std_kb)

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

            result = engine.query(prompt)
            body = json.dumps(result).encode('utf-8')

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

            table_rows = "".join([
                f"<tr><td>{r.get('timestamp_s')}s</td><td>{r.get('rpm_motor')}</td><td>{r.get('corrente_pack_a')} A</td><td>{r.get('bcm_tensao_v')} V</td><td>{r.get('tcm_pressao_bar')} bar</td><td>{r.get('bpcm_isolamento_kohm')} kΩ</td><td>{r.get('status_falha')}</td></tr>"
                for r in rows
            ])

            html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarleyOS | Scientific RAG & Systems Engineering</title>
    <style>
        :root {{
            --bg: #07090e; --surface: rgba(18, 24, 38, 0.75); --border: rgba(0, 210, 255, 0.2);
            --cyan: #00d2ff; --green: #00ffaa; --red: #ff3366; --text: #e6edf3; --text-dim: #8b949e;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); padding: 14px; min-height: 100vh; }}
        header {{ display: flex; align-items: center; justify-content: space-between; padding-bottom: 12px; border-bottom: 1px solid var(--border); margin-bottom: 14px; }}
        .brand {{ font-weight: 800; font-size: 1.1rem; color: var(--cyan); }}
        .grid-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 14px; }}
        .stat-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 10px; }}
        .stat-title {{ font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase; }}
        .stat-val {{ font-size: 1.25rem; font-weight: 700; margin-top: 4px; color: #fff; }}
        .glass-panel {{ background: var(--surface); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; margin-bottom: 14px; }}
        #chat-window {{ height: 350px; overflow-y: auto; background: rgba(10, 14, 22, 0.95); border-radius: 8px; padding: 12px; border: 1px solid rgba(0, 210, 255, 0.15); font-size: 0.83rem; display: flex; flex-direction: column; gap: 12px; }}
        .msg-bubble {{ padding: 12px; border-radius: 8px; max-width: 98%; line-height: 1.45; }}
        .msg-user {{ align-self: flex-end; background: rgba(0, 210, 255, 0.2); border: 1px solid rgba(0, 210, 255, 0.4); color: #fff; }}
        .msg-bot {{ align-self: flex-start; background: rgba(0, 255, 170, 0.06); border: 1px solid rgba(0, 255, 170, 0.25); color: #e1e7ec; width: 100%; }}
        .svg-container {{ margin: 10px 0; overflow-x: auto; }}
        pre {{ background: #05070a; padding: 10px; border-radius: 6px; overflow-x: auto; color: #00d2ff; font-family: monospace; font-size: 0.78rem; margin: 8px 0; border: 1px solid #1f2a3a; }}
        .input-box {{ display: flex; gap: 8px; margin-top: 10px; }}
        input {{ flex: 1; padding: 12px; background: rgba(12, 17, 28, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); color: #fff; border-radius: 6px; outline: none; font-size: 0.85rem; }}
        button {{ padding: 12px 18px; background: linear-gradient(135deg, #00d2ff 0%, #0072ff 100%); border: none; border-radius: 6px; color: #fff; font-weight: 700; cursor: pointer; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.75rem; margin: 8px 0; }}
        th, td {{ border: 1px solid rgba(255, 255, 255, 0.08); padding: 6px 8px; text-align: left; }}
        th {{ background: rgba(15, 22, 36, 0.9); color: var(--text-dim); text-transform: uppercase; }}
    </style>
</head>
<body>
    <header>
        <div class="brand">🔬 MarleyOS | Expert Systems Engineering</div>
        <div style="font-size:0.75rem; color:var(--green);">BASE DE DADOS CONECTADA</div>
    </header>

    <div class="grid-stats">
        <div class="stat-card"><div class="stat-title">🏎️ Rotação</div><div class="stat-val">{cur_rpm} RPM</div></div>
        <div class="stat-card"><div class="stat-title">⚡ Carga Pack</div><div class="stat-val">{cur_curr} A</div></div>
        <div class="stat-card"><div class="stat-title">🛡️ Isolamento</div><div class="stat-val">{cur_iso} kΩ</div></div>
        <div class="stat-card"><div class="stat-title">⚠️ Status</div><div class="stat-val" style="font-size:0.85rem; color:{'var(--red)' if cur_stat!='NORMAL' else 'var(--green)'};">{cur_stat}</div></div>
    </div>

    <div class="glass-panel">
        <div id="chat-window">
            <div class="msg-bubble msg-bot">
                <b>Copilot:</b> Banco de conhecimento de modelagem conectado.<br>
                Consulte: <i>'Como montar um circuito abaixador no Simulink?'</i>, <i>'Como montar um elevador Boost?'</i> ou <i>'Como montar um somador?'</i>[span_0](start_span)[span_0](end_span).
            </div>
        </div>
        <div class="input-box">
            <input id="prompt-input" type="text" placeholder="Pergunte sobre um sistema ou bloco de simulação..." onkeydown="if(event.key==='Enter') send()">
            <button onclick="send()">Enviar</button>
        </div>
    </div>

    <div class="glass-panel">
        <strong style="font-size:0.85rem; color:var(--cyan);">Telemetria CAN Bus de Bordo</strong>
        <div style="overflow-x:auto; margin-top:8px;">
            <table>
                <thead><tr><th>Tempo</th><th>RPM</th><th>Corrente</th><th>BCM</th><th>TCM</th><th>BPCM</th><th>Status</th></tr></thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
    </div>

    <script>
        function markdownTableToHTML(md) {{
            const lines = md.trim().split('\\n');
            if (lines.length < 3) return md;
            let html = '<table><thead><tr>';
            lines[0].split('|').filter(c => c.trim()).forEach(c => {{
                html += `<th>${{c.trim()}}</th>`;
            }});
            html += '</tr></thead><tbody>';
            for (let i = 2; i < lines.length; i++) {{
                html += '<tr>';
                lines[i].split('|').filter(c => c.trim()).forEach(c => {{
                    html += `<td>${{c.trim().replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>').replace(/`(.*?)`/g, '<code>$1</code>')}}</td>`;
                }});
                html += '</tr>';
            }}
            html += '</tbody></table>';
            return html;
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

                let replyHtml = `<b>${{data.title}}</b><br><br>`;
                replyHtml += `<b>1. Resumo & Descrição:</b><br>${{data.summary}}<br><br>`;
                replyHtml += `<b>2. Blocos Simulink Necessários:</b><br>${{markdownTableToHTML(data.blocks_table)}}<br>`;
                replyHtml += `<b>3. Lógica de Funcionamento:</b><br>${{data.logic.replace(/\\n/g, '<br>')}}<br><br>`;
                if (data.svg) {{
                    replyHtml += `<b>4. Diagrama Esquemático:</b><br><div class="svg-container">${{data.svg}}</div><br>`;
                }}
                if (data.script) {{
                    replyHtml += `<b>5. Script de Automação (Simulink.SimulationInput):</b><pre><code>${{data.script}}</code></pre>`;
                }}

                win.innerHTML += `<div class="msg-bubble msg-bot">${{replyHtml}}</div>`;
            }} catch(e) {{
                win.innerHTML += `<div class="msg-bubble msg-bot" style="color:var(--red);">Erro no processamento da base de dados.</div>`;
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
    with ReusableTCPServer(("", PORT), DashboardHandler) as httpd:
        httpd.serve_forever()
