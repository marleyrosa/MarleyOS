# Solved Engineering Exercises — Chapters 1, 2 & 3

**Author:** Eng. Marley Rosa Luciano | **Program:** NexusMBD AI-Native Powertrain Suite

All values below reference physical repository constants: $p=4$, $\lambda_{pm}=0.08\text{ Wb}$ (MIL harness), $K_t=0.48\text{ Nm/A}$, pack capacity $14.8\text{ kWh}$ (`telemetry_feeder.py`), and maximum pressure limit $\text{Calib\_K0\_PressureMax} = 18\text{ bar}$.

---

## Chapter 1 — PMSM Dynamics & K0 Clutch Slip

### Exercise 1.1 — Quadrature Current $i_q$
Given $T_{em} = 170\text{ Nm}$ (initial torque demand during `P2_HYBRID_BOOST` in `telemetry_feeder.py`):

$$i_q = \frac{T_{em}}{K_t} = \frac{170}{0.48} = 354.17\text{ A}$$

Verification via the complete electromagnetic formulation:
$$T_{em} = 1.5 \cdot p \cdot \lambda_{pm} \cdot i_q = 1.5 \times 4 \times 0.08 \times 354.17 = 170.0\text{ Nm} \quad \text{[Verified]}$$

### Exercise 1.2 — K0 Clutch Slip Thermal Dynamics
Given a slip speed window $20 < \Delta\omega \le 150\text{ RPM}$ and pressure modulation from $2.0$ to $12.0\text{ bar}$.

For $\Delta\omega = 100\text{ RPM}$:
$$P_{bar} = 2.0 + \frac{150 - 100}{150 - 20} \times (12.0 - 2.0) = 2.0 + 3.85 = 5.85\text{ bar}$$

Frictional power dissipation, assuming transmitted torque $T = 150\text{ Nm}$:
$$\Delta\omega_{rad/s} = 100 \times \frac{2\pi}{60} = 10.47\text{ rad/s}$$
$$P_{diss} = T \times \Delta\omega_{rad/s} = 150 \times 10.47 = 1570.8\text{ W}$$

Over a slip window of $0.5\text{ s}$, dissipated energy is $E = 785.4\text{ J}$. With an effective clutch pack mass $m = 1.2\text{ kg}$ and specific heat capacity $c = 500\text{ J/(kg}\cdot\text{K)}$:

$$\Delta T = \frac{E}{m \cdot c} = \frac{785.4}{600} = 1.31\,^{\circ}\text{C}$$

---

## Chapter 2 — Coulomb Counting & Telemetry

### Exercise 2.1 — State of Charge (SoC) Estimation via Coulomb Counting
Pack capacity: $14.8\text{ kWh}$. Assumed nominal pack voltage of $240\text{ V}$:

$$Q_{Ah} = \frac{14800\text{ Wh}}{240\text{ V}} = 61.67\text{ Ah}$$

For a discharge current $I = 176.7\text{ A}$ sustained for $30\text{ s}$ ($0.00833\text{ h}$):

$$\Delta Ah = 176.7 \times 0.00833 = 1.47\text{ Ah}$$
$$\Delta \text{SoC}\% = \frac{1.47}{61.67} \times 100 = 2.39\%$$

Given initial $\text{SoC}_0 = 82.0\%$:

$$\text{SoC}_{final} = 82.0 - 2.39 = \mathbf{79.61\%}$$

---

## Chapter 3 — MCP Architecture & MIL Execution

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
The `--initialize-matlab-on-startup=true` flag prevents re-initializing the MATLAB engine on every tool call, reducing context token overhead and execution latency.

### Exercise 3.2 — K0 Pressure Sweep (Empirical Validation)
Execution of `.github/prompts/test_k0_pressure.prompt.md` in MATLAB R2026a:

| K0 Pressure (bar) | Residual Acceleration Peak ($\text{m/s}^2$) | Status |
| :---: | :---: | :---: |
| 12 | 0.0002983 | PASS |
| 16 | 0.0002983 | PASS |
| 20 | 0.0002983 | PASS |
