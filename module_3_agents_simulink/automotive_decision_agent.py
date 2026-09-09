from module_1_rag.rag_engine import load_source_registry, search_sources
from module_2_mcp.mcp_server import handle_rpc


class AutomotiveDecisionAgent:
    def __init__(self):
        self.registry = load_source_registry()

    def decide_route(self, query):
        text = query.lower()
        if any(token in text for token in ("simulink", "matlab", "calibr", "powertrain", "motor", "torque", "foc")):
            return "matlab"
        if any(token in text for token in ("carla", "apollo", "autoware", "autonom", "scenario", "perception", "planning")):
            return "simulation"
        return "rag"

    def route(self, query):
        route = self.decide_route(query)
        request = None
        if route == "matlab":
            request = {"method": "tools/call", "params": {"name": "get_telemetry_summary"}}
        elif route == "simulation":
            request = {"method": "tools/call", "params": {"name": "get_critical_events"}}
        return {
            "query": query,
            "route": route,
            "sources": search_sources(query),
            "mcp_request": request,
            "mcp_result": handle_rpc(request) if request else {"status": "rag_only"},
        }