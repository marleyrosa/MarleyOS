# Capítulo 2: Eletrificação, Máquinas Síncronas PMSM & Controle FOC (BEV)

---

## 1. Visão Geral & Objetivos de Aprendizagem

Neste capítulo da formação **NexusMBD**, você dominará o projeto, controle vetorial e validação em Model-Based Design de um sistema de tração elétrico baseado no **Motor Síncrono de Ímãs Permanentes de Fluxo Radial (PMSM)** alimentado por inversor trifásico de alta tensão com chaveamento SVPWM.

### Objetivos Quantificáveis (Taxonomia de Bloom):
* **Compreender:** O eletromagnetismo de enrolamentos distribuídos e o princípio das forças de Lorentz e relutância que geram torque no rotor de ímãs permanentes.
* **Derivar:** As transformadas ortogonais de **Clarke** ($abc \to \alpha\beta$) e **Park** ($\alpha\beta \to dq$) invariantes em amplitude e potência.
* **Projetar:** O controle por orientação de campo (**Field-Oriented Control - FOC**) desacoplando o fluxo no eixo direto ($I_d$) da produção de torque no eixo em quadratura ($I_q$).
* **Sintonizar:** As malhas de corrente PI analiticamente com proteção anti-windup e desacoplamento de forças contra-eletromotrizes (*Back-EMF*).
* **Validar:** A operação nominal do inversor em $350\text{ V}$ barramento DC gerando corrente de pico de $238\text{ A}$ a $311\text{ Hz}$.

---

## 2. Nomenclatura e Parâmetros da Máquina Elétrica

| Parâmetro | Descrição | Unidade (SI) | Valor Nominal (NexusMBD PMSM) |
| :--- | :--- | :--- | :--- |
| $V_{dc}$ | Tensão do Barramento de Alta Tensão (HV DC Bus) | $\text{V}$ | $350.0 \text{ V}$ |
| $R_s$ | Resistência Estatórica por Fase | $\Omega$ | $0.038 \ \Omega$ |
| $L_d$ | Indutância de Eixo Direto (Direct Axis Inductance) | $\text{H}$ | $0.00045 \text{ H}$ ($0.45 \text{ mH}$) |
| $L_q$ | Indutância de Eixo em Quadratura (Quadrature Inductance) | $\text{H}$ | $0.00062 \text{ H}$ ($0.62 \text{ mH}$) |
| $\psi_{pm}$ | Fluxo Magnético Enlaçado dos Ímãs Permanentes | $\text{Wb}$ | $0.082 \text{ Wb}$ |
| $p$ | Número de Pares de Polos | $-$ | $4 \text{ pares}$ ($8 \text{ polos}$) |
| $I_{q,\max}$ | Corrente Máxima em Quadratura | $\text{A}_{rms}$ | $200.0 \text{ A}$ (Pico: $282.8 \text{ A}$) |
| $T_{em,\max}$| Torque Eletromagnético Máximo | $\text{N}\cdot\text{m}$ | $185.0 \text{ N}\cdot\text{m}$ |
| $\omega_e$ | Frequência Angular Elétrica | $\text{rad/s}$ | $\omega_e = p \cdot \omega_m$ |
| $f_e$ | Frequência Elétrica Fundamental | $\text{Hz}$ | $0 \text{ a } 350 \text{ Hz}$ ($311\text{ Hz}$ a $4665\text{ RPM}$) |

---

## 3. Fundamentação Matemática do Controle Vetorial FOC

No referencial estatórico trifásico natural ($abc$), as correntes e indutâncias são variantes no tempo em função da posição do rotor $\theta_e$:

$$[v_{abc}] = R_s [i_{abc}] + \frac{d}{dt} [\lambda_{abc}(\theta_e)]$$

Para viabilizar controle linear por reguladores PI clássicos, o controle FOC converte sinais senoidais alternados em grandezas contínuas no tempo (DC-like).

```mermaid
graph LR
    A[Correntes Trifásicas ia, ib, ic] -->|Transformada de Clarke| B[Eixo Estacionário iα, iβ]
    B -->|Transformada de Park θe| C[Eixos Síncronos id, iq]
    C --> D[Malhas de Corrente PI Decoupled]
    D -->|Park Inversa θe| E[Tensões vα, vβ]
    E -->|Modulador SVPWM| F[Ponte Inversora Trifásica HV]
```

### 3.1. Transformada de Clarke Invariante em Amplitude ($abc \to \alpha\beta0$)
$$i_\alpha = \frac{2}{3} \left( i_a - \frac{1}{2} i_b - \frac{1}{2} i_c \right) = i_a$$
$$i_\beta = \frac{2}{3} \left( \frac{\sqrt{3}}{2} i_b - \frac{\sqrt{3}}{2} i_c \right) = \frac{1}{\sqrt{3}} (i_b - i_c)$$

### 3.2. Transformada de Park ($ \alpha\beta \to dq $)
Rotaciona o referencial fixo pelo ângulo elétrico do rotor $\theta_e = \int \omega_e \, dt$:

$$\begin{bmatrix} i_d \\ i_q \end{bmatrix} = \begin{bmatrix} \cos\theta_e & \sin\theta_e \\ -\sin\theta_e & \cos\theta_e \end{bmatrix} \begin{bmatrix} i_\alpha \\ i_\beta \end{bmatrix}$$

### 3.3. Equações Diferenciais de Tensão no Rotor ($dq$)
$$\frac{di_d}{dt} = \frac{1}{L_d} \Big( v_d - R_s i_d + \omega_e L_q i_q \Big)$$
$$\frac{di_q}{dt} = \frac{1}{L_q} \Big( v_q - R_s i_q - \omega_e (L_d i_d + \psi_{pm}) \Big)$$

O termo $\omega_e (L_d i_d + \psi_{pm})$ é a **Força Contra-Eletromotriz (Back-EMF)**, e os termos cruzados $\omega_e L_q i_q$ e $\omega_e L_d i_d$ são compensados via desacoplamento *feedforward* nos controladores.

### 3.4. Equação de Produção de Torque Eletromagnético
$$T_{em} = \frac{3}{2} p \Big( \psi_{pm} i_q + (L_d - L_q) i_d i_q \Big)$$

Em máquinas de polos salientes ($L_d < L_q$), o termo $(L_d - L_q) i_d i_q$ é o **Torque de Relutância**. Operando com $i_d < 0$ (injeção no semi-eixo negativo), obtém-se o regime de **Enfraquecimento de Campo** (*Flux Weakening*) e aproveitamento máximo do torque de relutância (estratégia MTPA - *Maximum Torque Per Ampere*).

---

## 4. Arquitetura MBD nos 4 Solvers Simulink

No modelo [`Model/MIL_MarleyOS_Powertrain.slx`](file:///C:/Users/UsuarioPC/MarleyOS/Model/MIL_MarleyOS_Powertrain.slx), o subsistema elétrico está integrado aos 4 Solvers:

1. **`COMUNICACAO` (10 ms):**
   * Decodifica a requisição de torque do pedal: `EM_TORQUE_REQ_NM` do barramento CAN.
   * Valida sinais de temperatura do inversor IGBT e tensão de barramento HV.
2. **`SOFTECU` (100 µs / 10 kHz):**
   * Implementa as transformadas de Clarke/Park e o algoritmo MTPA que calcula os setpoints $i_d^*$ e $i_q^*$.
   * Executa os reguladores PI com desacoplamento de Back-EMF e modulação SVPWM com injeção de 3º harmônico.
3. **`MDL` (10 µs contínuo / Solver ode4):**
   * Modela as indutâncias não lineares $L_d(i_d, i_q)$ e $L_q(i_d, i_q)$ com mapa 2D de saturação magnética.
   * Modela as perdas por chaveamento nos IGBTs ($P_{sw}$) e condução ($P_{cond}$) para predição térmica do inversor.
4. **`OUT` (100 ms):**
   * Empacota no barramento CAN os sinais `PMSM_IQ_A`, `PMSM_RPM`, `INVERTER_TEMP_C` e `BUS_VOLTAGE_V`.

---

## 5. Laboratório Prático Guiado (Hands-On Lab 2)

### Objetivo:
Sintonizar as malhas de corrente PI via script MATLAB e validar a resposta a degrau de torque no motor PMSM.

### Procedimento no Repositório:
1. Abra e execute a rotina de calibração:
```matlab
run('export_pmsm_calibration.m')
```
2. O script calcula analiticamente os ganhos pelo critério de cancelamento de polo:
   $$K_{p,d} = \omega_{bw} \cdot L_d \qquad K_{i,d} = \omega_{bw} \cdot R_s$$
   $$K_{p,q} = \omega_{bw} \cdot L_q \qquad K_{i,q} = \omega_{bw} \cdot R_s$$
   onde $\omega_{bw} = 2\pi \cdot f_{bw}$ com largura de banda $f_{bw} = 500\text{ Hz}$.
3. Verifique o arquivo exportado com a matriz de calibração sintonizada.
4. Execute `python test_pipeline.py` para garantir que o modelo integrado passa nos testes unitários com erro RMS de corrente $< 1.5\%$.

---

## 6. Exercícios Técnicos Resolvidos

### Exercício 1: Cálculo do Torque com MTPA
**Enunciado:** Um motor PMSM com $p=4$, $\psi_{pm} = 0.082\text{ Wb}$, $L_d = 0.45\text{ mH}$ e $L_q = 0.62\text{ mH}$ opera com corrente de quadratura $i_q = 200\text{ A}$ e corrente de enfraquecimento de campo $i_d = -40\text{ A}$. Calcule:
* (a) O torque gerado pelo ímã permanente ($T_{mag}$).
* (b) O torque gerado pela relutância magnética ($T_{rel}$).
* (c) O torque total resultante ($T_{em}$).

**Solução:**
**(a) Torque magnético:**
$$T_{mag} = \frac{3}{2} p \, \psi_{pm} \, i_q = \frac{3}{2} \times 4 \times 0.082 \times 200 = 6 \times 0.082 \times 200 = \mathbf{98.4\text{ N}\cdot\text{m}}$$

**(b) Torque de relutância:**
$$T_{rel} = \frac{3}{2} p (L_d - L_q) i_d i_q = 6 \times (0.00045 - 0.00062) \times (-40) \times 200$$
$$T_{rel} = 6 \times (-0.00017) \times (-8000) = 6 \times 1.36 = \mathbf{8.16\text{ N}\cdot\text{m}}$$

**(c) Torque total:**
$$T_{em} = T_{mag} + T_{rel} = 98.4 + 8.16 = \mathbf{106.56\text{ N}\cdot\text{m}}$$

---

## 7. 💯 Rubrica de Avaliação do Módulo 2 (100 Pontos)

| Critério de Avaliação | Pontuação Máxima | Métrica de Verificação |
| :--- | :--- | :--- |
| **1. Dedução Analítica FOC** | 20 pontos | Resolução correta das transformadas Clarke/Park e cálculo do ângulo elétrico. |
| **2. Calibração dos Ganhos PI** | 30 pontos | Execução de `export_pmsm_calibration.m` gerando $K_p, K_i$ com largura de banda de $500\text{ Hz}$. |
| **3. Teste Unitário MIL** | 30 pontos | Validação em `test_pipeline.py` com erro de rastreamento de torque $< 3\%$. |
| **4. Exercício Teórico MTPA** | 20 pontos | Resolução do problema de cálculo do torque eletromagnético e relutância. |
| **TOTAL DO MÓDULO 2** | **100 PONTOS** | **Nota mínima de corte: 70 pontos** |
