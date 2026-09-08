# Diretrizes de Automação Simulink para o MarleyOS (via MATLAB MCP Server)

Sempre que gerar ou editar scripts de automação do MATLAB/Simulink neste repositório, siga estritamente os padrões de Model-Based Design:

1. **Uso Exclusivo de Simulink.SimulationInput**:
   - Nunca use `sim(modelName, 'ExternalInput', ...)` ou defina variáveis globais soltas no `base workspace`.
   - Crie instâncias limpas com: `simIn = Simulink.SimulationInput(modelName);`.
   - Modifique parâmetros ou sinais usando `simIn = simIn.setVariable('varName', valor);`.

2. **Formato de Dados Estruturado (Dataset)**:
   - Configure o modelo para salvar saídas no formato `Dataset`:
     `simIn = simIn.setModelParameter('SaveFormat', 'Dataset');`
     `simIn = simIn.setModelParameter('SaveOutput', 'on');`
   - Recupere sinais exclusivamente através de `simOut.logsout.get('sinal').Values`.

3. **Integração com Telemetria**:
   - Todo script de simulação dinâmico de trem de força deve exportar seus vetores temporais diretamente para o arquivo:
     `module_2_mcp/data/can_telemetry.csv`
   - O cabeçalho obrigatório do CSV é:
     `timestamp_s,rpm,torque_nm,throttle_pct,iq_a,modo_propulsao,status_motor`
