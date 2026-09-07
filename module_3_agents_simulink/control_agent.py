import csv
import os

class AutonomousTuningAgent:
    def __init__(self, telemetry_path):
        self.telemetry_path = telemetry_path
        self.max_current_limit = 300.0

    def run(self):
        print(f"[Agente] Lendo telemetria em: {self.telemetry_path}")
        if not os.path.exists(self.telemetry_path):
            print("[Agente] Erro: Arquivo de telemetria ausente.")
            return

        with open(self.telemetry_path, 'r') as f:
            data = list(csv.DictReader(f))

        currents = [float(row['corrente_pack_a']) for row in data]
        max_curr = max(currents)
        print(f"[Agente] Pico de corrente detectado: {max_curr} A")

        if max_curr > self.max_current_limit:
            print(f"[Agente] Limite de {self.max_current_limit} A excedido! Gerando ajuste para Simulink...")
            script_out = "module_3_agents_simulink/calibrated_control.m"
            matlab_code = f"""% Script de Ajuste Automatico via Agente de IA
set_param('Powertrain_Control/Inverter_Drive', 'UpperCurrentLimit', '{self.max_current_limit}');
set_param('Powertrain_Control/PID_Torque', 'Kp', '1.15');
set_param('Powertrain_Control/PID_Torque', 'Ki', '0.04');
simOut = sim('Powertrain_Control', 'StopTime', '2.5');
disp('Calibracao concluida com corte de saturacao.');
"""
            with open(script_out, 'w', encoding='utf-8') as f:
                f.write(matlab_code)
            print(f"[Agente] Script gerado em: {script_out}")
