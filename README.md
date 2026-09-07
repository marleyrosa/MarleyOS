# MarleyOS — Automotive AI Cockpit & Systems Engineering Engine

Plataforma aberta de Inteligência Artificial aplicada à Engenharia Automotiva, Diagnóstico de Bordo (OBD-II), Protocolo MCP, Sistemas Embarcados e Validação Funcional (ISO 26262).

---

## 🚘 Módulos e Subsistemas Monitorados

| Componente | Função Primária | Sinais & Protocolos | Nível ASIL (ISO 26262) |
| :--- | :--- | :--- | :--- |
| **Inversor de Tração** | Controle de ponte trifásica e torque EV | Corrente de Fase, Temperatura IGBT | ASIL-D |
| **Freio Regenerativo (ABS)** | Distribuição de frenagem mecânica/elétrica | Pressão Eletro-Hidráulica (Bar) | ASIL-D |
| **Direção Elétrica (EPS)** | Assistência dinâmica e retorno ativo | Torque de Coluna (Nm), Corrente Motor | ASIL-C |
| **ECM** | Controle de injeção e atuador de borboleta | Posição TPS (%), Pressão MAP (kPa) | ASIL-D |
| **BCM** | Gateway de carroceria e cargas secundárias | Tensão de Barramento (V), Relés | ASIL-B / QM |
| **TCM** | Controle eletro-hidráulico de marchas | Pressão de Linha (Bar), Embreagem | ASIL-C |
| **BPCM (HV BMS)** | Monitoramento de células e segurança de alta tensão | Resistência de Isolamento (kΩ), Pyro-Fuse | ASIL-D |

---

## 🛠️ Arquitetura Técnica de IA

* **RAG Engine (Módulo 1):** Vetorização e recuperação semântica de manuais técnicos e códigos DTC.
* **CAN MCP Server (Módulo 2):** Servidor JSON-RPC expondo telemetria no padrão Model Context Protocol.
* **ReAct Tuning Agent & Simulink (Módulo 3):** Agente integrado ao MATLAB MCP Core Server para calibração autônoma com Simulink.SimulationInput.
* **ASIL Evaluator (Módulo 4):** Validação estruturada sob a norma ISO 26262 com datasets JSONL.
* **CI/CD MLOps (Módulo 5):** Suíte de testes automatizada com auditoria de Pull Requests via GitHub Actions.
* **Cockpit Web Interativo (Módulo 6):** Dashboard com visual glassmorphism, orbe pulsante de status e copilot automotivo.

---

## 🚀 Como Executar

### 1. Inicialização Completa
```bash
./start_marleyos.sh
python exports/export_audit.py
