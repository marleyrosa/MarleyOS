# Teste K0

Execute uma varredura MIL de `Calib_K0_PressureMax` em `[12, 16, 20]` bar.

- Use `Simulink.SimulationInput`.
- Use `simIn.setVariable('Calib_K0_PressureMax', value)`.
- Execute com `sim(simIn)`.
- Extraia somente de `simOut.logsout.get('deceleration_residual').Values`.
- Retorne apenas uma tabela com pressão, pico residual e `PASS/FAIL`.
