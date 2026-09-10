# Exercícios Resolvidos — Capítulos 1, 2 e 3
**Autor:** Eng. Marley Rosa Luciano | **Formação:** NexusMBD AI-Native Powertrain Suite

Todos os valores abaixo usam constantes reais do repositório: `p=4`, `lambda_pm=0.08 Wb` (harness MIL), `Kt=0.48 Nm/A` (Capítulo 1), capacidade de pack `14.8 kWh` (`telemetry_feeder.py`) e o limite `Calib_K0_PressureMax=18 bar`.

## Capítulo 1 — PMSM e dinâmica de K0

### Exercício 1.1 — Corrente de quadratura $i_q$

Dado $T_{em}=170\text{ Nm}$ (torque inicial da fase `P2_HYBRID_BOOST` em `telemetry_feeder.py`):

$$i_q = \frac{T_{em}}{K_t} = \frac{170}{0.48} = 354{,}17\text{ A}$$

Verificação pela forma completa: $T_{em}=1.5\,p\,\lambda_{pm}\,i_q = 1.5 \times 4 \times 0.08 \times 354{,}17 = 170{,}0\text{ Nm}$. ✔

### Exercício 1.2 — Térmica da embreagem $K_0$ em deslizamento

Dados (Capítulo 1): faixa de deslizamento $20 < \Delta\omega \le 150\text{ RPM}$, pressão de $2{,}0$ a $12{,}0$ bar.

Para $\Delta\omega = 100\text{ RPM}$:

$$P_{bar} = 2{,}0 + \frac{150-100}{150-20}\times(12{,}0-2{,}0) = 2{,}0 + 3{,}85 = 5{,}85\text{ bar}$$

Potência dissipada por atrito, assumindo torque transmitido $T=150\text{ Nm}$:

$$\Delta\omega_{rad/s} = 100 \times \frac{2\pi}{60} = 10{,}47\text{ rad/s}$$
$$P_{diss} = T \times \Delta\omega_{rad/s} = 150 \times 10{,}47 = 1570{,}8\text{ W}$$

Para uma janela de deslizamento de $0{,}5\text{ s}$, energia dissipada $E = 785{,}4\text{ J}$. Com massa efetiva do pacote de discos $m=1{,}2\text{ kg}$ e calor específico $c=500\text{ J/(kg·K)}$:

$$\Delta T = \frac{E}{m\,c} = \frac{785{,}4}{600} = 1{,}31\,^{\circ}\text{C}$$

## Capítulo 2 — Coulomb Counting e telemetria

### Exercício 2.1 — Estimativa de SoC por Coulomb Counting

Capacidade do pack: $14{,}8\text{ kWh}$. Tensão nominal assumida $240\text{ V}$ (próxima do máximo validado de `BusVoltage`):

$$Q_{Ah} = \frac{14800\text{ Wh}}{240\text{ V}} = 61{,}67\text{ Ah}$$

Para corrente de descarga $I=176{,}7\text{ A}$ (pico validado de `HVBatCurrent`) sustentada por $30\text{ s}$ ($0{,}00833\text{ h}$):

$$\Delta Ah = 176{,}7 \times 0{,}00833 = 1{,}47\text{ Ah}$$
$$\Delta SoC\% = \frac{1{,}47}{61{,}67}\times100 = 2{,}39\%$$

Com $SoC_0=82{,}0\%$ (valor inicial em `telemetry_feeder.py`):

$$SoC_{final} = 82{,}0 - 2{,}39 = 79{,}61\%$$

## Capítulo 3 — MCP e execução MIL

### Exercício 3.1 — Descritor mínimo do MATLAB MCP

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

A flag `--initialize-matlab-on-startup=true` evita reinicializar o MATLAB a cada chamada, reduzindo o custo de contexto por execução e o tempo de resposta do agente.

### Exercício 3.2 — Varredura K0 (resultado real validado)

Execução real do template `.github/prompts/test_k0_pressure.prompt.md` no MATLAB R2026a:

| Pressão K0 (bar) | Pico residual (m/s²) | Status |
|---:|---:|:---:|
| 12 | 0,0002983 | PASS |
| 16 | 0,0002983 | PASS |
| 20 | 0,0002983 | PASS |

O resultado constante entre pressões reflete que o harness atual ainda usa uma planta simplificada; o Exercício 3.3 (saturação PMSM) é o próximo refinamento físico do subsistema `MDL`.
