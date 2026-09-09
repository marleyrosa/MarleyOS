# Capítulo 3 — MBD, Agentes e MATLAB MCP

## Objetivo

Este capítulo define o ciclo mínimo de automação MIL do MarleyOS: sinais de comunicação entram como `Dataset`, calibrações são isoladas em `Simulink.SimulationInput` e os resultados saem por `logsout` para o Cockpit.

## Arquitetura 4 Mains

| Main | Responsabilidade | Contrato |
|---|---|---|
| COMUNICACAO | CAN/CSV/DBC e entradas externas | `CommunicationDataset` |
| SOFTECU | K0, e-DCT, ECM, TCM e BPCM | calibrações via `setVariable` |
| MDL | PMSM, inércia, rodas e perdas | sinais físicos calculados |
| SISTEMA | logging e métricas | `logsout` em formato Dataset |

## Execução MIL sem estado global

```matlab
simIn = Simulink.SimulationInput('MIL_MarleyOS_Powertrain');
simIn = simIn.setVariable('Calib_K0_PressureMax', 16.0);
simIn = simIn.setModelParameter( ...
    'StopTime', '1', ...
    'SaveFormat', 'Dataset', ...
    'SaveOutput', 'on', ...
    'SignalLogging', 'on', ...
    'SignalLoggingName', 'logsout');
simOut = sim(simIn);
residual = simOut.logsout.get('deceleration_residual').Values;
```

O wrapper [run_4mains_mil.m](../module_3_agents_simulink/run_4mains_mil.m) aplica o mesmo contrato e injeta o Dataset de comunicação sem modificar o workspace base.

## Agente e prompt templates

Os templates em `.github/prompts/` mantêm as instruções curtas: o agente recebe uma calibração, executa a simulação e devolve somente métricas e `PASS/FAIL`. O template K0 corresponde ao runner [run_k0_pressure_sweep.m](../module_3_agents_simulink/run_k0_pressure_sweep.m), que varre 12, 16 e 20 bar.

## Integração MCP e Cockpit

O endpoint `POST /api/run-mil` gera o DBC default, converte a telemetria atual em Dataset e dispara o MATLAB de forma assíncrona. O polling em `GET /api/run-mil` retorna o estado, código de retorno e métricas serializadas pelo runner.

## Critérios de validação

- O modelo deve gerar `logsout` com sinais nomeados.
- A alteração de calibração deve ocorrer via `SimulationInput.setVariable`.
- A execução deve ser reproduzível com o Dataset de comunicação.
- O Cockpit deve exibir estado e métricas sem bloquear o servidor HTTP.