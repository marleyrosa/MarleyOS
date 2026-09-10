# NexusMBD // AI-Native Powertrain Engineering Suite

<div align="center" style="margin: 20px 0;">
  <p style="font-size: 1.1rem; color: #f0f6fc; font-weight: bold; margin-bottom: 8px;">Author: Eng. Marley Rosa Luciano</p>
  <span style="border: 1px solid #00e5ff; color: #00e5ff; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-family: monospace; background: rgba(0,229,255,0.1); margin-right: 6px;">[MCP] CAN Protocol</span>
  <span style="border: 1px solid #b388ff; color: #b388ff; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-family: monospace; background: rgba(179,136,255,0.1); margin-right: 6px;">[RAG] Knowledge Base</span>
  <span style="border: 1px solid #ff9100; color: #ff9100; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-family: monospace; background: rgba(255,145,0,0.1); margin-right: 6px;">[AGENTS] Simulink MBD</span>
  <span style="border: 1px solid #00e676; color: #00e676; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-family: monospace; background: rgba(0,230,118,0.1);">[FINE-TUNING] ISO 26262</span>
</div>

---

## 🚀 About the Program & Platform

The **NexusMBD Engineering Suite** is an advanced educational and practical ecosystem designed to empower automotive systems engineers in the mathematical modeling, control, and validation of state-of-the-art powertrains (**ICE, BEV, and P2 Hybrids**).

The curriculum bridges high-fidelity **Model-Based Design (MBD)** in MATLAB/Simulink with the 4 frontiers of Artificial Intelligence:

1. **[MCP] Model Context Protocol:** JSON-RPC tool server decoding industrial CAN DBC streams and serving 100ms real-time telemetry to Large Language Models (LLMs).
2. **[RAG] Retrieval-Augmented Generation:** Vectorized engineering knowledge base with P2 topology schematics, high-voltage workshop manuals, and structured diagnostic trouble code (DTC) procedures.
3. **[AGENTS] Simulink MIL Automation:** Autonomous ReAct agents orchestrating the 4 Mains solvers (`COMUNICACAO`, `SOFTECU`, `MDL`, `OUT`), tuning PI current loops, and executing batch simulations.
4. **[FINE-TUNING] LLM Domain Model:** Foundation models adapted with proprietary vehicle dynamics datasets and functional safety verification rules under **ISO 26262 (ASIL-D)**.

---

## 📚 Course Curriculum Map

```mermaid
graph TD
    A[Module 1: Thermal ICE Dynamics & Miller Cycle] --> B[Module 2: BEV Electric Traction & FOC Vector Control]
    B --> C[Module 3: P2 Hybrid Architecture, EMS & K0 Clutch]
    C --> D[Module 4: MCP Protocol & Real-Time CAN DBC Streaming]
    D --> E[Module 5: RAG & DTC Decision Fault Trees]
    E --> F[Module 6: Autonomous Simulink Calibration Agents]
    F --> G[Module 7: Fine-Tuning & ISO 26262 Safety Auditing]
    G --> H[Module 8: Integrated Capstone Project & Certification]
```

---

## 🖥️ Live Telemetry Web Cockpit

The platform features an interactive real-time telemetry cockpit operating locally and accessible across devices on the local network:
* **Local Web URL (PC):** `http://localhost:8080`
* **Executive Master Slides (English):** `http://localhost:8080/slides-en`
* **Official Digital Certificate:** `http://localhost:8080/certificado`
* **Termux Android Integration:** Stream raw CAN frames via `curl -s http://localhost:8080/api/telemetry | jq .`
