import json
import csv
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TELEMETRY_PATH = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")

def _value(row, *names, default=0.0):
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return value
    return default

def tool_get_telemetry_summary():
    if not os.path.exists(TELEMETRY_PATH):
        return {"error": "Arquivo nao encontrado"}
    with open(TELEMETRY_PATH, 'r') as f:
        rows = list(csv.DictReader(f))
    rpms = [float(_value(r, "rpm_motor", "rpm_em", "rpm_ice")) for r in rows]
    currents = [float(_value(r, "corrente_pack_a", "torque_nm")) for r in rows]
    temps = [float(_value(r, "temp_inversor_c", "temp_inv_c")) for r in rows]
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
            if _value(r, "status_falha", "status_motor", default="NORMAL") != 'NORMAL':
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
