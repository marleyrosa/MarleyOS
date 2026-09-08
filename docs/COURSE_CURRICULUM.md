# MarleyOS: Engenharia de Propulsão Híbrida P2 & Automação MBD com Agentes

## Ementa do Treinamento

Capacitação no projeto, modelagem, telemetria e validação de trens de força híbridos paralelos (P2), integrando telemetria leve com o ecossistema de Model-Based Design (MATLAB/Simulink via MCP Server).

### Módulo 1: Arquitetura Híbrida Paralela P2 e Modelagem Física
* Arranjo mecânico coaxial: ICE 1.5L Miller, embreagem K0 e máquina síncrona PMSM.
* Controle Orientado a Campo (FOC) e curva MTPA torque x corrente de quadratura.
* Dinâmica hidráulica da K0: fases Open, Slipping e Locked (18 bar).
* Transmissão e-DCT dual-shaft: embreagens concêntricas C1 (ímpar) e C2 (par).

### Módulo 2: Instrumentação Digital, Barramento CAN e Cockpit Web
* Barramento CAN contínuo a 10 Hz via can_telemetry.csv.
* Dinâmica de bateria (SoC %), gestão térmica do inversor e BSFC do motor térmico.
* Medidor inercial G-Bowl (-1.5G a +1.5G) e pedais físicos reativos 3D.
* Data logger integrado com exportação direta em CSV.

### Módulo 3: Model-Based Design & Automação com Agentes MCP
* Padrão Simulink.SimulationInput e extração Dataset (logsout).
* Configuração do MATLAB MCP Core Server no VS Code (.vscode/mcp.json).
* Inicialização persistente com a flag --initialize-matlab-on-startup=true.
