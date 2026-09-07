import json
import csv
import os

TELEMETRY_PATH = "module_2_mcp/data/can_telemetry.csv"

def tool_get_telemetry_summary():
    if not os.path.exists(TELEMETRY_PATH):
        return {"error": "Arquivo nao encontrado"}
    with open(TELEMETRY_PATH, 'r') as f:
        rows = list(csv.DictReader(f))
    rpms = [float(r['rpm_motor']) for r in rows]
    currents = [float(r['corrente_pack_a']) for r in rows]
    temps = [float(r['temp_inversor_c']) for r in rows]
    return {
        "amostras": len(rows),
        "rpm_max": max(rpms),
        "corrente_max_a": max(currents),
        "temp_max_c": max(temps)
    }

def tool_get_critical_events():
    if not os.path.exists(TELEMETRY_PATH):
        return {"error": "Arquivo nao encontrado"}
    critical = []
    with open(TELEMETRY_PATH, 'r') as f:
        for r in csv.DictReader(f):
            if r['status_falha'] != 'NORMAL':
                critical.append(r)
    return {"eventos_criticos": critical}

TOOLS = {
    "get_telemetry_summary": tool_get_telemetry_summary,
    "get_critical_events": tool_get_critical_events
}

def handle_rpc(payload):
    method = payload.get("method")
    if method == "tools/list":
        return {"tools": list(TOOLS.keys())}
    elif method == "tools/call":
        name = payload.get("params", {}).get("name")
        return TOOLS.get(name, lambda: {"error": "not found"})()
    return {"error": "invalid method"}

if __name__ == "__main__":
    print("[MCP Server] Ferramentas ativas:", handle_rpc({"method": "tools/list"}))
    print("[MCP Server] Telemetria:", handle_rpc({"method": "tools/call", "params": {"name": "get_telemetry_summary"}}))
