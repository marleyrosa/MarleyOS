# 🛸 Implementation Plan: Orbital Paper Lab (Antigravity Swarm)

> **Task Slug:** `orbital-paper-lab`  
> **Target:** Transform the Kiotopaper notebook & paper draft into an interactive orbital simulation with a 3D WebGL radial scene and real-time autonomous swarm agent execution panels.  
> **Source Context:** Antigravity Master Plan / Notebook Kiotopaper

---

## 🎯 Architectural Overview

- **Core (Gravitational Center):** Manuscript State (LaTeX, Equations, MBD Models, Python/Simulink code, HIL Bench logs).
- **Orbital Ring / Graph:** 10 candidate journals/conferences (IEEE, SAE, Elsevier, IFAC, etc.) with metadata (APC, deadlines, acceptance scores, requirements).
- **Agent Swarm Dispatcher:** 5 asynchronous agents (`AG-01` to `AG-05`) with live telemetry and data stream loops.
- **UI Architecture (Split Screen Dashboard):**
  - **Top:** Three.js / WebGL accelerated 3D Orbital Scene (radial graph, central pulsating core, particle streams, interactive orbit rings).
  - **Bottom:** 8-module mission control dark terminal grid (Extraction Pipeline, Particle/Simulation Solver, Method Workspace, HIL Validation Metrics, Swarm Dispatcher, Journal Fit Matrix, Budget/APC Tracker, Timeline/Deadlines).

---

## 📋 Task Breakdown & Agent Assignments

### Phase 1: Environment & Knowledge Base Setup (RAG / Data Layer)
- [x] **Task 1.1: Dependency & Project Scaffold Setup**
  - Install runtime dependencies (Three.js, Lucide icons, math/charting utilities).
  - Assigned to: `devops-engineer`
  - Verification: `npm list three` and development server launches without errors.
- [x] **Task 1.2: Journal Knowledge Base & Manuscript Models (`data/`)**
  - Create structured JSON/TypeScript schemas for 10 journals (IEEE TTE, SAE WCX, Elsevier CEP, IFAC, etc.), requirements, APC models, and Kiotopaper state.
  - Assigned to: `backend-specialist` / `database-architect`
  - Verification: Schema validation passes with mock data.

### Phase 2: WebGL Orbital 3D Visualizer (`components/orbital/`)
- [x] **Task 2.1: Three.js Radial Canvas Core**
  - Build central glowing pulsar node with dynamic bloom and shader/particle field.
  - Assigned to: `frontend-specialist`
  - Verification: 60 FPS rotation, responsive resize, smooth camera orbit controls.
- [x] **Task 2.2: Orbital Rings & Target Journal Nodes**
  - Render concentric orbital paths, 10 interactive conference nodes with status halos, and pulse beams connecting core to orbits.
  - Assigned to: `frontend-specialist`
  - Verification: Hovering/clicking nodes inspects journal compliance and updates telemetry.
- [x] **Task 2.3: Real-Time Particle Data Streams**
  - Trigger luminous pulses along orbital bezier curves when swarm agents dispatch or return results.
  - Assigned to: `frontend-specialist`
  - Verification: Visual feedback triggers dynamically upon agent cycle completion.

### Phase 3: Bottom Control Grid & 8 Mission Control Submodules
- [x] **Task 3.1: Dashboard Layout & Theme Token System**
  - Implement high-density, dark sci-fi/aerospace terminal theme with CSS variables and monospace typography.
  - Assigned to: `frontend-specialist`
  - Verification: Strict theme adherence, zero overflow, responsive 8-grid layout.
- [x] **Task 3.2: Modules 1–4 (Extraction, Solver, Method, HIL Metrics)**
  - Extraction Pipeline: LaTeX parsing progress & equation count.
  - Simulation Solver: Canvas for ADAS/propulsion transient response curves.
  - Method Workspace: Code editor view showing agent-generated Kalman/MPC algorithms.
  - Validation Metrics: Real-time HIL/MIL residual error charts.
  - Assigned to: `frontend-specialist`
  - Verification: Dynamic canvas/SVG rendering with live parameter updates.
- [x] **Task 3.3: Modules 5–8 (Swarm Dispatcher, Matrix, Budget, Countdown)**
  - Swarm Dispatcher: AG-01 through AG-05 asynchronous status indicators and event log.
  - Journal Fit Matrix: Heatmap matrix of compatibility scores across 10 journals.
  - Budget & APC Tracker: Multi-currency converter (USD/EUR/BRL) and OA model toggle.
  - Timeline & Deadlines: Real-time countdown clocks to SAE WCX, IEEE, etc.
  - Assigned to: `frontend-specialist`
  - Verification: Real-time clock ticks, interactive currency switcher, reactive state.

### Phase 4: Swarm Dispatcher Engine & Loop Integration
- [x] **Task 4.1: Agent Swarm State Machine (`services/swarm/`)**
  - Implement simulated autonomous event loop for AG-01..AG-05 with controllable dispatch intervals (Normal / Fast / Step).
  - Assigned to: `backend-specialist`
  - Verification: State transitions emit events that simultaneously update 3D particles and terminal panels.
- [x] **Task 4.2: Kiotopaper Document Reactive Sync**
  - Allow user to edit abstract/parameters and observe real-time score updates across the 10 journals.
  - Assigned to: `frontend-specialist`
  - Verification: Input changes immediately trigger AG-01 and AG-03 re-scoring.

### Phase X: Final Verification & Performance Profiling
- [x] **Task X.1: End-to-End Visual & Functional Audit**
  - Verify WebGL canvas memory lifecycle, no WebGL context loss, 60 FPS performance, and error-free console.
  - Assigned to: `qa-automation-engineer` / `performance-optimizer`
  - Verification: Production build (`npm run build`) succeeds and all modules are fully interactive.

---

## 🔗 Agent & Skill Mapping

| Domain | Assigned Agent | Key Skills Applied |
|---|---|---|
| Planning & Orchestration | `project-planner` / `orchestrator` | `plan-writing`, `brainstorming`, `app-builder` |
| 3D WebGL & Dashboard UI | `frontend-specialist` | `frontend-design`, `frontend-architecture`, `design-spec` |
| Swarm Engine & Mock RAG | `backend-specialist` | `clean-code`, `api-patterns` |
| Verification & Performance | `qa-automation-engineer` | `verify-changes`, `webapp-testing` |
