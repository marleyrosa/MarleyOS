%% Síntese de Calibração: Torque x Iq (PMSM MTPA)
% Gera a tabela de calibração para consumo do módulo RAG / MCP

p = 4;              % Pares de polos
lambda_pm = 0.08;   % Fluxo concatenado do ímã (Wb)
iq_range = 0:10:250; % Faixa de 0 a 250 A

% Relação sob MTPA (id = 0, polos lisos): T_em = 1.5 * p * lambda_pm * iq
kt = 1.5 * p * lambda_pm; % Constante de torque (Nm/A)
torque_curve = kt * iq_range;

% Exportação em formato JSON estruturado para a base de conhecimento
outputPath = fullfile('..', 'module_1_rag', 'knowledge_base', 'pmsm_calibration_map.json');
fid = fopen(outputPath, 'w');

fprintf(fid, '{\n');
fprintf(fid, '  "machine_type": "PMSM",\n');
fprintf(fid, '  "kt_nm_per_a": %.4f,\n', kt);
fprintf(fid, '  "iq_amps": [%s],\n', num2str(iq_range, '%.1f, '));
fprintf(fid, '  "torque_nm": [%s]\n', num2str(torque_curve, '%.2f, '));
fprintf(fid, '}\n');
fclose(fid);

fprintf('[+] Mapa de calibração exportado com sucesso: %s\n', outputPath);
