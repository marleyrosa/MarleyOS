import unittest
import os
import csv
from module_2_mcp.mcp_server import handle_rpc

class TestAutomotiveAIEngine(unittest.TestCase):

    def test_01_csv_dtc_exists_and_populated(self):
        """Valida integridade da base de códigos DTC."""
        path = "module_1_rag/data/obd_dtc_codes.csv"
        self.assertTrue(os.path.exists(path), f"Arquivo {path} ausente")
        with open(path, 'r', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            self.assertGreater(len(reader), 0, "Base DTC vazia")

    def test_02_mcp_tool_execution(self):
        """Valida se o servidor MCP processa consultas de telemetria."""
        res = handle_rpc({"method": "tools/call", "params": {"name": "get_telemetry_summary"}})
        self.assertIn("corrente_max_a", res, "Servidor MCP nao retornou telemetria calculada")
        self.assertGreater(res["corrente_max_a"], 0, "Corrente deve ser positiva")

if __name__ == "__main__":
    unittest.main()
