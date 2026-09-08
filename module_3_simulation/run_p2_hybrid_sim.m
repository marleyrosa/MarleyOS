%% Automação de Simulação - Trem de Força Híbrido P2
% Padrão: Guy on Simulink (Simulink.SimulationInput + Dataset logsout)

modelName = 'P2_Hybrid_Powertrain';

% 1. Instanciação e parametrização do SimulationInput
simIn = Simulink.SimulationInput(modelName);
simIn = simIn.setModelParameter('SaveFormat', 'Dataset');
simIn = simIn.setModelParameter('SaveOutput', 'on');
simIn = simIn.setModelParameter('StopTime', '10.0');

% Injeção de variáveis de operação (demanda transitória)
simIn = simIn.setVariable('throttle_demand', 75.0);   % Demanda de 75%
simIn = simIn.setVariable('Iq_target', 180.0);         % Corrente de quadratura PMSM (A)
simIn = simIn.setVariable('ice_torque_target', 140.0); % Torque motor térmico (Nm)

% 2. Execução da Simulação
fprintf('[+] Executando simulação desacoplada do modelo: %s\n', modelName);
simOut = sim(simIn);

% 3. Extração dos sinais do Dataset logsout
logs = simOut.logsout;
time = logs.get('rpm').Values.Time;
rpm_data = logs.get('rpm').Values.Data;
torque_data = logs.get('torque_combined').Values.Data;
throttle_data = logs.get('throttle').Values.Data;

% 4. Exportação para a telemetria do Cockpit MarleyOS
outputPath = fullfile('..', 'module_2_mcp', 'data', 'can_telemetry.csv');
fid = fopen(outputPath, 'w');
fprintf(fid, 'timestamp_s,rpm,torque_nm,throttle_pct,iq_a,modo_propulsao,status_motor\n');

for k = 1:length(time)
    fprintf(fid, '%.2f,%.1f,%.1f,%.1f,180.0,P2_HYBRID_BOOST,NOMINAL\n', ...
        time(k), rpm_data(k), torque_data(k), throttle_data(k));
end
fclose(fid);
fprintf('[+] Telemetria gerada com sucesso em: %s\n', outputPath);
