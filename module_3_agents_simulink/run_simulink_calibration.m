% Script de Calibração Autônoma - MarleyOS & MATLAB MCP Server
modelName = 'Powertrain_Control';
disp(['[MarleyOS] Iniciando calibração do modelo: ' modelName]);

% Configuração da simulação usando padrão SimulationInput
simIn = Simulink.SimulationInput(modelName);
simIn = simIn.setVariable('MaxCurrentLimit', 285.0);
simIn = simIn.setVariable('Kp_Torque', 1.15);
simIn = simIn.setVariable('Ki_Torque', 0.04);
simIn = simIn.setModelParameter('StopTime', '2.5');

disp('[MarleyOS] Parâmetros atualizados via Agente ReAct. Pronto para simulação.');
