import json
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from module_3_agents_simulink.automotive_decision_agent import AutomotiveDecisionAgent


def run_marleyos_rag_agent_mcp_pipeline(query):
    result = AutomotiveDecisionAgent().route(query)
    return {
        "query": query,
        "route": result["route"],
        "sources": [source["name"] for source in result["sources"]],
        "mcp_request": result["mcp_request"],
        "mcp_result": result["mcp_result"],
    }


if __name__ == "__main__":
    query = "Como calibrar um controlador de torque em Simulink para EV?"
    print(json.dumps(run_marleyos_rag_agent_mcp_pipeline(query), ensure_ascii=False, indent=2))