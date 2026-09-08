import unittest
import os
from module_2_mcp.mcp_server import handle_rpc
from module_4_finetuning.iso_safety_validator import evaluate_functional_safety
from module_3_simulation.powertrain_models import ice_torque, pmsm_foc

class TestAutomotiveAIEngine(unittest.TestCase):
    def test_01_csv_dtc_exists(self):
        self.assertTrue(os.path.exists("module_1_rag/data/obd_dtc_codes.csv"))

    def test_02_mcp_tool_execution(self):
        res = handle_rpc({"method": "tools/call", "params": {"name": "get_telemetry_summary"}})
        self.assertIn("corrente_max_a", res)

    def test_03_iso26262_asil(self):
        res = evaluate_functional_safety("Falha: Corrente do pack atingiu 315A excedendo limiar de 300A.")
        self.assertIn("ASIL-D", res)

    def test_04_ice_torque_and_bsfc(self):
        point = ice_torque(75.0, 2500.0)
        self.assertGreater(point.torque_nm, 0.0)
        self.assertGreater(point.bsfc_g_kwh, 0.0)

    def test_05_bev_foc_id_iq(self):
        point = pmsm_foc(120.0, 3000.0)
        self.assertAlmostEqual(point.id_a, 0.0)
        self.assertGreater(point.iq_a, 0.0)
        self.assertGreater(point.electrical_power_kw, 0.0)

if __name__ == "__main__":
    unittest.main()
