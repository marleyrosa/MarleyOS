# MarleyOS — Automotive AI Architecture & Cognitive Learning Manual

**Author:** Eng. Marley Rosa Luciano | **Program:** NexusMBD AI-Native Powertrain Suite

This document outlines the internal architecture of **MarleyOS**, an engineering operating system combining cognitive AI agents, the Model Context Protocol (MCP), and closed-loop Model-in-the-Loop (MIL) simulation.

---

## 🧠 Cognitive Agent Learning Cycle

1. **Sensing & Ingestion:** Ingesting 100ms CAN telemetry frames via the JSON-RPC MCP server.
2. **Diagnosis (RAG Engine):** Grounded identification of DTC faults from technical manuals without hallucination.
3. **Safety Assessment (ISO 26262):** Automated evaluation of ASIL levels (QM to ASIL-D) and fail-safe state transition.
4. **Actuation & Calibration (Agent Toolkit):**
   - ReAct agent creates modern `Simulink.SimulationInput` objects for the MATLAB MCP Core Server.
   - The agent verifies that controller retuning suppresses physical transients before approving calibration tables.
5. **Pedagogical Synthesis:** The agent articulates the mathematical and thermodynamic rationale behind each engineering decision.

---

## ⚙️ MATLAB & Simulink MCP Integration Guidelines
- **Workspace Isolation:** Parameter calibrations are injected via `.setVariable()` into the Model Workspace.
- **Structured I/O:** Telemetry extraction must use `Simulink.SimulationData.Dataset` structures (`logsout`).
- **Headless Execution:** Utilize `-batch` commands and `sim(in)` objects rather than legacy GUI-bound commands.
