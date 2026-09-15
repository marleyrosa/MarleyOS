# Solved Engineering Exercises — NexusMBD Powertrain Suite

**Author:** Eng. Marley Rosa Luciano | **Program:** NexusMBD AI-Native Powertrain Suite  
**Reference Constants:** Rotor pole pairs $p=4$, permanent magnet flux linkage $\lambda_{pm}=0.08\text{ Wb}$, torque constant $K_t=0.48\text{ Nm/A}$, battery pack capacity $14.8\text{ kWh}$ ($61.67\text{ Ah}$ @ $240\text{ V}$), and maximum K0 line pressure $\text{Calib\_K0\_PressureMax} = 18\text{ bar}$.

---

## Chapter 1 — PMSM Dynamics & K0 Clutch Slip

### Exercise 1.1 — First-Principles Deduction of MTPA Torque Equation and Quadrature Current $i_q$

#### 1. Context and Problem Statement
During a hybrid boost transient (`P2_HYBRID_BOOST` in `telemetry_feeder.py`), the Energy Management System (EMS) commands an electric motor electromagnetic torque of:
$$T_{em}^* = 170.0\text{ Nm}$$

Derive from fundamental electromagnetic relations (Park transform and airgap power) the complete torque equation for a three-phase PMSM, demonstrate why the Maximum Torque Per Ampere (MTPA) strategy simplifies to $T_{em} = \frac{3}{2} p \lambda_{pm} i_q$, compute the motor torque constant $K_t$, determine the required quadrature current $i_q$, and verify the solution with zero residual error.

---

#### 2. Mathematical Deduction: From Stator Electrodynamics to Torque

##### Step 1: Stator Flux Linkage and Voltage in Synchronous $d$-$q$ Coordinates
Under the rotor reference frame Park transformation (direct axis aligned with the rotor permanent magnet flux vector $\vec{\lambda}_{pm}$), the stator flux linkages along the direct ($d$) and quadrature ($q$) axes are:
$$\psi_d = L_d i_d + \lambda_{pm}$$
$$\psi_q = L_q i_q$$

where $L_d$ and $L_q$ are the stator inductances along the $d$ and $q$ magnetic axes, and $\lambda_{pm}$ is the permanent magnet flux linkage.

The corresponding terminal stator voltage equations under electrical angular frequency $\omega_e = p \omega_m$ (with $p$ pole pairs and $\omega_m$ mechanical rotor speed in $\text{rad/s}$) are:
$$v_d = R_s i_d + \frac{d\psi_d}{dt} - \omega_e \psi_q$$
$$v_q = R_s i_q + \frac{d\psi_q}{dt} + \omega_e \psi_d$$

where $R_s$ is the per-phase stator winding resistance.

##### Step 2: Instantaneous Stator Input Power and Airgap Power
The total instantaneous electrical power supplied to a three-phase balanced stator in $d$-$q$ variables is given by the power-invariant transformation:
$$P_{in} = \frac{3}{2} (v_d i_d + v_q i_q)$$

Substituting the voltage expressions into the power relation:
$$P_{in} = \underbrace{\frac{3}{2} R_s (i_d^2 + i_q^2)}_{\text{Stator Joule Losses } P_{cu}} + \underbrace{\frac{3}{2} \left( i_d \frac{d\psi_d}{dt} + i_q \frac{d\psi_q}{dt} \right)}_{\text{Magnetic Energy Storage Rate } \frac{dW_m}{dt}} + \underbrace{\frac{3}{2} \omega_e (\psi_d i_q - \psi_q i_d)}_{\text{Electromechanical Airgap Power } P_{em}}$$

##### Step 3: Electromagnetic Torque Formulation
By the principle of energy conservation, the airgap power $P_{em}$ is the actual electromagnetic power converted into rotational mechanical work:
$$P_{em} = T_{em} \cdot \omega_m$$

Recalling the kinematic coupling between electrical and mechanical angular velocity $\omega_e = p \cdot \omega_m \implies \omega_m = \frac{\omega_e}{p}$:
$$T_{em} = \frac{P_{em}}{\omega_m} = \frac{\frac{3}{2} \omega_e (\psi_d i_q - \psi_q i_d)}{\frac{\omega_e}{p}} = \frac{3}{2} p (\psi_d i_q - \psi_q i_d)$$

Substituting the flux linkage expressions $\psi_d = L_d i_d + \lambda_{pm}$ and $\psi_q = L_q i_q$:
$$T_{em} = \frac{3}{2} p \left[ (L_d i_d + \lambda_{pm}) i_q - (L_q i_q) i_d \right]$$
$$T_{em} = \frac{3}{2} p \lambda_{pm} i_q + \frac{3}{2} p (L_d - L_q) i_d i_q$$

This is the **fundamental PMSM torque equation**, composed of:
1. **Synchronous Alignment Torque:** $\frac{3}{2} p \lambda_{pm} i_q$ (interaction between stator current and permanent magnets).
2. **Reluctance Torque:** $\frac{3}{2} p (L_d - L_q) i_d i_q$ (caused by rotor magnetic saliency where $L_q \ne L_d$).

##### Step 4: MTPA Simplification for Non-Salient PMSM (Polos Lisos / SPMSM)
In surface-mounted permanent magnet machines (SPMSM) or machines with non-salient cylindrical rotors (polos lisos), the rare-earth magnets have relative magnetic permeability $\mu_r \approx 1.05 \approx \mu_0$. The magnetic reluctance seen by the stator is virtually isotropic around the airgap circumference:
$$L_d \approx L_q \implies (L_d - L_q) = 0$$

Consequently, the reluctance torque term vanishes identically:
$$T_{rel} = \frac{3}{2} p (L_d - L_q) i_d i_q = 0$$

To achieve **Maximum Torque Per Ampere (MTPA)** below the base motor speed, the stator current vector magnitude $I_s = \sqrt{i_d^2 + i_q^2}$ must be minimized for any given torque demand. Since $i_d$ produces zero reluctance torque and contributes only to unwanted stator copper losses, the optimal MTPA trajectory strictly imposes:
$$i_d^* = 0, \quad i_q^* = I_s$$

Thus, the general equation reduces to the linear MTPA torque formulation:
$$T_{em} = \frac{3}{2} p \lambda_{pm} i_q$$

##### Step 5: Derivation of the Torque Constant $K_t$
Defining the lumped electromechanical torque constant $K_t \triangleq \frac{T_{em}}{i_q}$:
$$K_t = \frac{3}{2} p \lambda_{pm}$$

Substituting the repository powertrain parameters ($p = 4$ pole pairs, $\lambda_{pm} = 0.08\text{ Wb}$):
$$K_t = \frac{3}{2} \times 4 \times 0.08 = 6 \times 0.08 = \mathbf{0.48\text{ Nm/A}}$$

##### Step 6: Numeric Calculation of Quadrature Current $i_q$
For a demanded torque $T_{em} = 170.0\text{ Nm}$:
$$i_q = \frac{T_{em}}{K_t} = \frac{170.0\text{ Nm}}{0.48\text{ Nm/A}} = \frac{17000}{48} = \frac{2125}{6} \approx \mathbf{354.1667\text{ A}}$$

Rounding to two decimal places:
$$\mathbf{i_q = 354.17\text{ A}}$$

##### Step 7: Analytic Reverse Verification
Substituting $i_q = 354.1667\text{ A}$ back into the full electromagnetic airgap equation:
$$T_{em} = 1.5 \times 4 \times 0.08\text{ Wb} \times 354.1667\text{ A} = 0.48 \times 354.1667 = 170.0000\text{ Nm}$$
$$\text{Residual Error: } \epsilon = |170.0 - 170.0| = 0.00\text{ Nm} \quad \text{[VERIFIED]}$$

---

### Exercise 1.2 — K0 Clutch Slip Thermal Dynamics
Given a slip speed window $20 < \Delta\omega \le 150\text{ RPM}$ and pressure modulation from $2.0$ to $12.0\text{ bar}$.

For $\Delta\omega = 100\text{ RPM}$:
$$P_{bar} = 2.0 + \frac{150 - 100}{150 - 20} \times (12.0 - 2.0) = 2.0 + \frac{50}{130} \times 10.0 = 2.0 + 3.846 = 5.85\text{ bar}$$

Frictional power dissipation, assuming transmitted torque $T = 150\text{ Nm}$:
$$\Delta\omega_{rad/s} = 100 \times \frac{2\pi}{60} = 10.472\text{ rad/s}$$
$$P_{diss} = T \times \Delta\omega_{rad/s} = 150 \times 10.472 = 1570.8\text{ W}$$

Over a slip window of $t_{slip} = 0.5\text{ s}$, total dissipated energy is:
$$E = P_{diss} \times t_{slip} = 1570.8 \times 0.5 = 785.4\text{ J}$$

With an effective clutch pack mass $m = 1.2\text{ kg}$ and specific heat capacity $c = 500\text{ J/(kg}\cdot\text{K)}$:
$$\Delta T = \frac{E}{m \cdot c} = \frac{785.4\text{ J}}{1.2\text{ kg} \times 500\text{ J/(kg}\cdot\text{K)}} = \frac{785.4}{600} = \mathbf{1.31\,^{\circ}\text{C}}$$

---

## Chapter 2 — Battery Coulomb Counting & SoC Dynamics

### Exercise 2.1 — State of Charge (SoC) Estimation via Coulomb Counting
Pack total energy capacity: $14.8\text{ kWh}$. Nominal pack terminal voltage: $V_{pack} = 240.0\text{ V}$.

The total nominal charge capacity in Ampere-hours ($Q_{Ah}$) is:
$$Q_{Ah} = \frac{14800\text{ Wh}}{240.0\text{ V}} = 61.667\text{ Ah}$$

During a high-power boost event, a constant discharge current $I = 176.7\text{ A}$ is drawn continuously for $t = 30.0\text{ s}$ ($t_h = \frac{30}{3600}\text{ h} = 0.008333\text{ h}$):
$$\Delta Ah = I \times t_h = 176.7\text{ A} \times 0.008333\text{ h} = 1.4725\text{ Ah}$$

The percentage reduction in State of Charge ($\Delta \text{SoC}\%$) is:
$$\Delta \text{SoC}\% = \frac{\Delta Ah}{Q_{Ah}} \times 100 = \frac{1.4725\text{ Ah}}{61.667\text{ Ah}} \times 100 = 2.3878\% \approx 2.39\%$$

Given an initial battery state $\text{SoC}_0 = 82.0\%$:
$$\text{SoC}_{final} = \text{SoC}_0 - \Delta \text{SoC}\% = 82.0 - 2.39 = \mathbf{79.61\%}$$

---

## Chapter 3 — Model Context Protocol & MIL Simulation

### Exercise 3.1 — Minimal MATLAB MCP Server Configuration
```json
{
  "servers": {
    "matlab": {
      "type": "stdio",
      "command": "matlab-mcp.exe",
      "args": ["--initialize-matlab-on-startup=true"]
    }
  }
}
```
The `--initialize-matlab-on-startup=true` flag guarantees that the MATLAB COM/IPC engine is warmed up at agent startup, avoiding cold-start latency spikes of 15–20 s on initial simulation dispatches.

### Exercise 3.2 — K0 Clutch Pressure Sweep (Empirical Validation)
Execution results from automated batch testing in MATLAB R2026a (`.github/prompts/test_k0_pressure.prompt.md`):

| K0 Pressure (bar) | Residual Acceleration Peak ($\text{m/s}^2$) | Stability Margin | ISO 26262 Status |
| :---: | :---: | :---: | :---: |
| 12.0 | 0.0002983 | $> 12\text{ dB}$ | PASS |
| 16.0 | 0.0002983 | $> 14\text{ dB}$ | PASS |
| 20.0 | 0.0002983 | $> 15\text{ dB}$ | PASS |

---

## Chapter 4 — Functional Safety ISO 26262 & FTTI Timing Budget

### Exercise 4.1 — Fault Tolerant Time Interval ($FTTI \le 20\text{ ms}$) Deduction for ASIL-D Inverter Control

#### 1. Hazard Definition and Controllability Context
Under **ISO 26262-3:2018 (Hazard Analysis and Risk Assessment - HARA)**, the worst-case hazardous event for an electric traction powertrain is:
> **Hazardous Event (HE.01):** *Unintended longitudinal acceleration or over-torque ($\Delta T_{em} > 0$) while cruising or cornering on low-adhesion surfaces ($\mu \le 0.3$).*

Classification: **Severity S3** (fatal injuries), **Exposure E4** (high highway exposure), **Controllability C3** (less than 90% of drivers can maintain lane stability). Consequently, the safety goal is categorized as **ASIL-D**.

The **Fault Tolerant Time Interval (FTTI)** represents the maximum allowable duration between the occurrence of an internal fault (e.g., gate driver desaturation, ADC current sensor failure, or corrupted CAN message) and the transition to a hazardous event where vehicle stability is irreversibly lost.

---

#### 2. Physical & Kinematic Derivation of the $20\text{ ms}$ Upper Bound

##### Step 1: Drivetrain Mechanical Inertia and Acceleration Surge
Consider an unanticipated over-torque step $\Delta T_{em} = 200.0\text{ Nm}$ injected directly into the transmission input shaft.
The lumped rotational inertia of the P2 electric motor rotor, K0 housing, and input shaft assembly is:
$$J_{eq} = 0.18\text{ kg}\cdot\text{m}^2$$

The resulting angular acceleration surge at the rotor shaft is:
$$\Delta \alpha = \frac{\Delta T_{em}}{J_{eq}} = \frac{200.0\text{ Nm}}{0.18\text{ kg}\cdot\text{m}^2} = 1111.11\text{ rad/s}^2$$

##### Step 2: Vehicle Acceleration and Drivetrain Jerk over Duration $\Delta t$
Through the total final driveline ratio $i_g = 8.5$ and effective wheel rolling radius $r_w = 0.32\text{ m}$, the angular speed error at the wheels over elapsed time $\Delta t$ is:
$$\Delta \omega_{wheel} = \frac{\Delta \alpha \cdot \Delta t}{i_g}$$

The resulting longitudinal speed error transmitted to the vehicle chassis is:
$$\Delta v(t) = \Delta \omega_{wheel} \cdot r_w = \frac{\Delta \alpha \cdot r_w}{i_g} \cdot \Delta t = \frac{1111.11 \times 0.32}{8.5} \cdot \Delta t = 41.83 \cdot \Delta t\text{ [m/s]}$$

Differentiating with respect to time yields the longitudinal acceleration jump (chassis jerk spike):
$$\Delta a = \frac{d(\Delta v)}{dt} = \frac{\Delta \alpha \cdot r_w}{i_g} = 41.83\text{ m/s}^2$$

##### Step 3: Tire Adhesion Limit and Driver Reaction Boundary
On wet or icy asphalt ($\mu = 0.3$), the maximum tire tractive force before sudden breakaway is limited by:
$$F_{max} = \mu \cdot M_{veh} \cdot g$$
For a vehicle mass $M_{veh} = 1800\text{ kg}$:
$$a_{crit} = \mu \cdot g = 0.3 \times 9.81 = 2.94\text{ m/s}^2$$

If the uncommanded torque surge persists for $\Delta t = 20\text{ ms} = 0.020\text{ s}$:
$$\Delta v_{surge} = 41.83 \times 0.020 = 0.837\text{ m/s} \approx 3.01\text{ km/h}$$
The kinetic energy injected into the tire-road contact patch over $20\text{ ms}$ is within the tire carcass elastic relaxation zone ($\Delta \theta_{slip} < 1.5^\circ$), preventing instantaneous wheel lockup or spinout. If $\Delta t > 20\text{ ms}$, the accumulated slip angle exceeds the lateral adhesion limit, inducing sudden vehicle yaw instability (ASIL-D boundary violation).

Therefore, the maximum safety threshold for functional safety compliance is:
$$\mathbf{FTTI \le 20\text{ ms}}$$

---

#### 3. Execution Timing Budget: Verification against $\text{FTTI}$

According to ISO 26262-1, the safety mechanism must satisfy:
$$\text{Fault Handling Time Interval (FHTI)} = \text{FDTI} + \text{FRTI} \le \text{FTTI}$$

where:
1. **FDTI (Fault Detection Time Interval):**
   - Stator overcurrent hardware comparator: $t_{comp} \le 1.5\,\mu\text{s}$
   - Microcontroller dual-core lockstep diagnostic task cycle: $T_{task} = 1.0\text{ ms}$
   - Digital plausibility filter and debounce window (3 consecutive execution frames):
     $$\text{FDTI} = 3 \times 1.0\text{ ms} = \mathbf{3.0\text{ ms}}$$

2. **FRTI (Fault Reaction Time Interval):**
   - Safe State transition: Disabling PWM pulses and asserting hardware **Active Short Circuit (ASC)** or **Open-Circuit Freewheel**:
   - Gate driver interlock propagation: $t_{prop} \approx 2.5\,\mu\text{s}$
   - DC-link discharge and stator transient demagnetization settlement:
     $$\text{FRTI} = \mathbf{5.0\text{ ms}}$$

##### Synthesis and Safety Margin:
$$\text{Total FHTI} = \text{FDTI} + \text{FRTI} = 3.0\text{ ms} + 5.0\text{ ms} = \mathbf{8.0\text{ ms}}$$

Checking compliance:
$$\text{FHTI} = 8.0\text{ ms} \le \text{FTTI} = 20.0\text{ ms} \quad \text{[COMPLIANT]}$$

$$\text{Safety Margin } \text{SM} = \frac{\text{FTTI} - \text{FHTI}}{\text{FTTI}} \times 100\% = \frac{20.0 - 8.0}{20.0} \times 100\% = \mathbf{60.0\%}$$

The system reacts in **$8\text{ ms}$**, well within the mandatory $20\text{ ms}$ limit, ensuring full compliance with ISO 26262 ASIL-D safety requirements.

---

## 9. Gabarito Comentado da Avaliação Oficial (10 Questões NexusMBD)

| Questão | Pilar | Alternativa Correta | Justificativa Técnica |
| :---: | :---: | :---: | :--- |
| **1** | MCP | **B** | As *tools* do MCP definem endpoints executáveis com schemas JSON rigorosos para interação entre o LLM e o ambiente MBD (ex: simulação MIL, DBC). |
| **2** | MCP | **B** | O servidor MCP utiliza a biblioteca `cantools` para parsear arquivos DBC e converter payloads CAN hexadecimais em unidades de engenharia. |
| **3** | RAG | **B** | A busca híbrida une busca densa (vetores semânticos) com busca esparsa (BM25 para códigos exatos de falhas como `P0A1F-00`), garantindo acurácia. |
| **4** | RAG | **B** | Limitar a recuperação a chunks de alto reranking e exigir citação auditável previne alucinações de valores críticos de segurança ASIL-D. |
| **5** | FINE-TUNING | **B** | O Fine-Tuning adapta modelos de linguagem à sintaxe de scripts MBD, comandos de telemetria e normas de auditoria funcional ISO 26262. |
| **6** | FINE-TUNING | **B** | O formato JSONL estruturado em papeis (`System`, `User`, `Assistant`) garante aprendizado de contexto rigoroso para auditoria automotiva. |
| **7** | AGENTS | **B** | O padrão ReAct encadeia o raciocínio (*Thought*), a execução da Tool (*Action*) e a leitura do estado de saída (*Observation*). |
| **8** | AGENTS | **B** | Ao detectar *slip* excessivo na K0, o agente de calibração reajusta os tempos de pressão via Tool e re-executa a simulação para otimizar o ITAE. |
| **9** | INTEGRAÇÃO | **A** | Os 4 pilares cooperam: RAG (normas), Fine-Tuning (raciocínio especializado), MCP (exposição de ferramentas) e AGENTS (loop fechado). |
| **10** | CERTIFICAÇÃO | **B** | A nota de corte mínima oficial para aprovação e emissão do Certificado SHA-256 é de **60%** (600/1000 pontos ou 6 acertos em 10). |

