# MarleyOS: Planner de Treinamento (ICE, HEV e BEV)

Status: concluído no repositório. A validação executável está em `test_pipeline.py`.

## 4 Areas
- MCP: matlab-mcp-core-server, SimulationInput e Dataset.
- Agent: Inspecao de parametros e chaveamento de torque.
- RAG: Base simulink_systems.json com esquemas SVG.
- Fine-Tuning: Boas praticas MBD e dinamica eletromecanica.

## Modulos
1. ICE: Dinamica de torque, admissao e BSFC. Implementado em `module_3_simulation/powertrain_models.py`.
2. BEV: Motor sincrono PMSM, FOC e malhas id/iq. Implementado em `module_3_simulation/powertrain_models.py` e `export_pmsm_calibration.m`.
3. HEV: Hibrido P2, EMS e embreagem. Implementado em `p2_mode_supervisor.m`, `k0_clutch_controller.m` e `run_p2_hybrid_sim.m`.
4. MCP: Automacao de simulacao em lote. Implementado em `.vscode/mcp.json`, `module_2_mcp/mcp_server.py` e scripts MATLAB.
5. Cockpit MarleyOS: Integrador final Termux. Implementado em `dashboard/server.py`, `telemetry_feeder.py` e `run.sh`.
