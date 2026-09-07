import unittest
import os
from module_2_mcp.mcp_server import handle_rpc
from module_4_finetuning.iso_safety_validator import evaluate_functional_safety

class TestAutomotiveAIEngine(unittest.TestCase):
    def test_01_csv_dtc_exists(self):
        self.assertTrue(os.path.exists("module_1_rag/data/obd_dtc_codes.csv"))

    def test_02_mcp_tool_execution(self):
        res = handle_rpc({"method": "tools/call", "params": {"name": "get_telemetry_summary"}})
        self.assertIn("corrente_max_a", res)

    def test_03_iso26262_asil(self):
        res = evaluate_functional_safety("Falha: Corrente do pack atingiu 315A excedendo limiar de 300A.")
        self.assertIn("ASIL-D", res)

if __name__ == "__main__":
    unittest.main()
