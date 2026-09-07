import csv
import os

class AutonomousTuningAgent:
    def __init__(self, telemetry_path):
        self.telemetry_path = telemetry_path
        self.max_current_limit = 285.0

    def run(self):
        print(f"[Agente] Lendo telemetria CAN: {self.telemetry_path}")
        if not os.path.exists(self.telemetry_path):
            print("[Agente] Telemetria não encontrada.")
            return

        with open(self.telemetry_path, 'r', encoding='utf-8') as f:
            data = list(csv.DictReader(f))

        currents = [float(row.get('corrente_pack_a', 0.0)) for row in data]
        max_curr = max(currents)
        print(f"[Agente] Pico de corrente identificado: {max_curr} A")

        # Gerar script executável pelo MATLAB MCP Server
        script_out = "module_3_agents_simulink/run_simulink_calibration.m"
        matlab_code = f"""% Script de Calibração Autônoma - MarleyOS & MATLAB MCP Server
modelName = 'Powertrain_Control';
disp(['[MarleyOS] Iniciando calibração do modelo: ' modelName]);

% Configuração da simulação usando padrão SimulationInput
simIn = Simulink.SimulationInput(modelName);
simIn = simIn.setVariable('MaxCurrentLimit', {self.max_current_limit});
simIn = simIn.setVariable('Kp_Torque', 1.15);
simIn = simIn.setVariable('Ki_Torque', 0.04);
simIn = simIn.setModelParameter('StopTime', '2.5');

disp('[MarleyOS] Parâmetros atualizados via Agente ReAct. Pronto para simulação.');
"""
        with open(script_out, 'w', encoding='utf-8') as f:
            f.write(matlab_code)
        print(f"[Agente] Rotina MATLAB sintetizada em: {script_out}")

if __name__ == "__main__":
    import sys
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    telemetry = os.path.join(ROOT, "module_2_mcp", "data", "can_telemetry.csv")
    agent = AutonomousTuningAgent(telemetry)
    agent.run()
