# NexusMBD // AI-Native Powertrain Engineering Suite

<div align="center" style="margin: 20px 0;">
  <p style="font-size: 1.1rem; color: #f0f6fc; font-weight: bold; margin-bottom: 8px;">Autor: Eng. Marley Rosa Luciano</p>
  <span style="border: 1px solid #00e5ff; color: #00e5ff; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-family: monospace; background: rgba(0,229,255,0.1); margin-right: 6px;">[MCP] CAN Protocol</span>
  <span style="border: 1px solid #b388ff; color: #b388ff; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-family: monospace; background: rgba(179,136,255,0.1); margin-right: 6px;">[RAG] Knowledge Base</span>
  <span style="border: 1px solid #ff9100; color: #ff9100; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-family: monospace; background: rgba(255,145,0,0.1); margin-right: 6px;">[AGENTS] Simulink MBD</span>
  <span style="border: 1px solid #00e676; color: #00e676; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-family: monospace; background: rgba(0,230,118,0.1);">[FINE-TUNING] ISO 26262</span>
</div>

---

## 🚀 Sobre o Curso & A Plataforma

A **NexusMBD Engineering Suite** é um ecossistema educacional e prático projetado para capacitar engenheiros de sistemas automotivos no desenvolvimento, modelagem matemática, controle e validação de trens de força modernos (**ICE, BEV e Híbridos P2**).

A metodologia conecta o **Model-Based Design (MBD)** de alta fidelidade no MATLAB/Simulink às 4 fronteiras da Inteligência Artificial:

1. **[MCP] Model Context Protocol:** Servidor JSON-RPC que decodifica barramentos CAN DBC e expõe canais de telemetria contínuos como ferramentas (*tool calls*) para Grandes Modelos de Linguagem (LLMs).
2. **[RAG] Retrieval-Augmented Generation:** Base de conhecimento técnico vetorial com esquemas de topologia P2, manuais de alta tensão e procedimentos estruturados para isolamento de códigos de falha (DTCs).
3. **[AGENTS] Simulink MIL Automation:** Agentes ReAct autônomos que orquestram os solvers 4 Mains (`COMUNICACAO`, `SOFTECU`, `MDL`, `OUT`), ajustam parâmetros de malhas de corrente PI e executam testes em lote.
4. **[FINE-TUNING] LLM Domain Model:** Modelos de linguagem adaptados com datasets proprietários de dinâmica veicular e regras de segurança funcional segundo a **ISO 26262 (ASIL-D)**.

---

## 📚 Estrutura da Formação

```mermaid
graph TD
    A[Módulo 1: Dinâmica Térmica ICE & Miller Cycle] --> B[Módulo 2: Tração Elétrica BEV & FOC Vector Control]
    B --> C[Módulo 3: Arquitetura Híbrida P2, EMS & K0 Clutch]
    C --> D[Módulo 4: Protocolo MCP & Streaming CAN DBC]
    D --> E[Módulo 5: RAG & Árvores de Diagnóstico DTC]
    E --> F[Módulo 6: Agentes Autônomos de Calibração Simulink]
    F --> G[Módulo 7: Capstone Integrado & Auditoria de Segurança]
```

---

## 🖥️ Cockpit de Telemetria ao Vivo

O sistema conta com um cockpit telemétrico interativo a 60 FPS servido localmente e acessível por dispositivos móveis na mesma rede:
* **URL Local (PC):** `http://localhost:8080`
* **URL Móvel (Wi-Fi):** `http://192.168.1.22:8080`
* **Integração Termux (Android):** Consumo de fluxo CAN via `curl -s http://192.168.1.22:8080/api/telemetry | jq .`
