% Script de Ajuste Automatico via Agente de IA
set_param('Powertrain_Control/Inverter_Drive', 'UpperCurrentLimit', '300.0');
set_param('Powertrain_Control/PID_Torque', 'Kp', '1.15');
set_param('Powertrain_Control/PID_Torque', 'Ki', '0.04');
simOut = sim('Powertrain_Control', 'StopTime', '2.5');
disp('Calibracao concluida com corte de saturacao.');
