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

## Arquitetura MIL: 4 Mains

1. **COMUNICACAO**: CAN/DBC, REST, Inport e Dataset.
2. **SOFTECU**: ECM, TCM, BPCM e DCDC parametrizados.
3. **MDL**: planta eletromecânica, PMSM, embreagens, rodas e resistências.
4. **SISTEMA**: `logsout`, métricas e exportação para o dashboard.

## Regras de baixo consumo de contexto

- Use `Simulink.SimulationInput` e `sim(simIn)` para runners MIL.
- Use `simIn.setVariable()` para calibrações e `setModelParameter()` para parâmetros de modelo.
- Configure `SaveFormat='Dataset'`, `SaveOutput='on'` e `SignalLoggingName='logsout'`.
- Extraia sinais de `simOut.logsout.get('sinal').Values`.
- Não use `load_system`, `exist()`, `evalin('base')`, `assignin` ou shell em runners MIL.
- Converta CSV de comunicação com `module_2_mcp/load_dbc_signals.m`.
