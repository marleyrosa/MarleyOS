%% Teste de Degrau da Malha de Corrente Iq (PMSM FOC)
% Diretrizes: Guy on Simulink (Simulink.SimulationInput + Dataset logsout)

modelName = 'PMSM_FOC_CurrentLoop';

% Parametros da maquina e malha
p = 4;              % Pares de polos
lambda_pm = 0.08;   % Fluxo do ima permanente (Wb)
Rs = 0.05;          % Resistencia estatorica (Ohms)
Lq = 0.00035;       % Indutancia de quadratura (H)

% Ganhos PI (resposta temporal de malha fechada ~ 2 ms)
tau_loop = 0.002;
Kp_iq = Lq / tau_loop;
Ki_iq = Rs / tau_loop;

% 1. Instanciação e desacoplamento do modelo
simIn = Simulink.SimulationInput(modelName);
simIn = simIn.setModelParameter('SaveFormat', 'Dataset');
simIn = simIn.setModelParameter('SaveOutput', 'on');
simIn = simIn.setModelParameter('StopTime', '0.1');

% Injeção de variáveis da malha de quadratura
simIn = simIn.setVariable('Kp_q', Kp_iq);
simIn = simIn.setVariable('Ki_q', Ki_iq);
simIn = simIn.setVariable('Iq_step_ref', 180.0); % Degrau de 180 A (Boost)

% 2. Execucao da simulacao
fprintf('[+] Iniciando ensaio de resposta ao degrau da malha Iq...\n');
simOut = sim(simIn);

% 3. Avaliacao do erro em regime
logs = simOut.logsout;
iq_measured = logs.get('iq_meas').Values.Data;
time = logs.get('iq_meas').Values.Time;

steady_iq = iq_measured(end);
fprintf('[+] Resposta final Iq: %.2f A (Alvo: 180.0 A)\n', steady_iq);
