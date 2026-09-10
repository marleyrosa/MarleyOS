# MarleyOS — Arquitetura de IA Automotiva & Manual de Aprendizagem
**Autor:** Eng. Marley Rosa Luciano | **Formação:** NexusMBD AI-Native Powertrain Suite

Este documento descreve o funcionamento interno do **MarleyOS**, concebido como um sistema operacional de engenharia com agentes cognitivos, protocolo MCP e simulação em malha fechada.

---

## 🧠 Ciclo Cognitivo de Aprendizagem do Agente

1. **Percepção (Sensing):** Ingestão de telemetria CAN via servidor MCP (JSON-RPC).
2. **Diagnóstico (RAG Engine):** Identificação de falhas DTC em manuais técnicos sem alucinação.
3. **Julgamento de Segurança (ISO 26262):** Avaliação do nível ASIL (A a D) e definição do *Safe State*.
4. **Atuação & Sintonia (Agent Toolkit):**
   - Agente ReAct gera objetos modernos `Simulink.SimulationInput` para o MATLAB MCP Core Server.
   - O agente valida se a recalibração conteve o transiente físico antes de liberar para o veículo.
5. **Síntese Pedagógica:** O Copilot explica a razão matemática e física de cada intervenção de engenharia.

---

## ⚙️ Regras do MATLAB & Simulink MCP Integration
- **Isolamento de Variáveis:** Configurações de calibração são passadas via `.setVariable()`.
- **Entrada e Saída Estruturada:** Dados coletados devem utilizar o formato `Simulink.SimulationData.Dataset`.
- **Evitar Comandos Legados:** Nunca concatenar matrizes simples `[t u]` sem o método formal de simulação.
