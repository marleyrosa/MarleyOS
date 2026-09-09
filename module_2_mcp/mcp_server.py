import json
import csv
import os
import sys

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
    rpms = [float(_value(r, "rpm_motor", "rpm_em", "rpm_ice", "EMSpeed")) for r in rows]
    currents = [abs(float(_value(r, "corrente_pack_a", "battery_current_a", "HVBatCurrent", "torque_nm", "EMTrqReq"))) for r in rows]
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

def serve_stdio():
    for line in sys.stdin:
        if not line.strip():
            continue
        request = json.loads(line)
        method = request.get("method")

        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "marleyos-can", "version": "1.0.0"},
            }
        elif method == "notifications/initialized":
            continue
        elif method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": "get_telemetry_summary",
                        "description": "Retorna o resumo da telemetria CAN atual.",
                        "inputSchema": {"type": "object", "properties": {}},
                    },
                    {
                        "name": "get_critical_events",
                        "description": "Retorna eventos críticos da telemetria CAN.",
                        "inputSchema": {"type": "object", "properties": {}},
                    },
                ]
            }
        elif method == "tools/call":
            name = request.get("params", {}).get("name")
            result = {"content": [{"type": "text", "text": json.dumps(TOOLS.get(name, lambda: {"error": "not found"})(), ensure_ascii=False)}]}
        else:
            result = handle_rpc(request)

        print(json.dumps({"jsonrpc": "2.0", "id": request.get("id"), "result": result}, ensure_ascii=False), flush=True)

if __name__ == "__main__":
    serve_stdio()
