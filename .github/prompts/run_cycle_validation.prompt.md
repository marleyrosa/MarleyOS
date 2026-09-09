# Validacao de ciclo

Execute o ciclo default do MarleyOS com `Simulink.SimulationInput`.

- Configure `SaveFormat='Dataset'`, `SaveOutput='on'`, `SignalLoggingName='logsout'`.
- Extraia `iq_a` e `BSFC` via `simOut.logsout.get('<sinal>').Values`.
- Calcule pico de `iq_a` e maximo de `BSFC`.
- Retorne somente a tabela de metricas e o status final `PASS/FAIL`.
