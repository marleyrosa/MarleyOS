---
marp: true
theme: nexusmbd
paginate: true
header: "NexusMBD // AI-Native Powertrain Suite"
footer: "Módulo 1: Dinâmica Térmica ICE & Arquitetura MBD"
size: 16:9
---

<!-- _class: lead -->

# NEXUSMBD // SUITE EXECUTIVA
### AI-Native Powertrain Engineering Suite
Model-Based Design • P2 Hybrid Architecture • 4 Pilares de Inteligência Artificial

<div style="margin-top: 25px;">
  <span class="badge badge-cyan">[MCP] CAN Protocol</span>
  <span class="badge badge-amber">[RAG] Vector Manuals</span>
  <span class="badge badge-green">[AGENTS] Simulink MIL</span>
  <span class="badge badge-cyan">[FINE-TUNING] ISO 26262</span>
</div>

---

# A Visão: Engenharia MBD Acelerada por IA

<div class="card">
  <strong>O Desafio da Eletrificação Moderna:</strong>
  Projetar powertrains híbridos exige sincronizar termodinâmica de combustão, máquinas elétricas de alta rotação e controle de embreagens hidráulicas em milissegundos, sob estrita conformidade com a <strong>ISO 26262 (ASIL-D)</strong>.
</div>

<div class="grid-2">
  <div class="card">
    <h3>Engenharia MBD Clássica</h3>
    <ul>
      <li>Modelos matemáticos em Simulink</li>
      <li>Calibração manual exaustiva</li>
      <li>Documentação estática desconectada</li>
      <li>Depuração reativa de falhas</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>NexusMBD AI-Native</h3>
    <ul>
      <li>Solvers 4 Mains orquestrados por Agentes</li>
      <li>Calibração automatizada via MCP JSON-RPC</li>
      <li>RAG conectado a manuais e diagramas SVG</li>
      <li>Previsão e auditoria contínua de DTCs</li>
    </ul>
  </div>
</div>

---

# Os 4 Pilares da Arquitetura de IA

<div class="grid-4">
  <div class="card">
    <span class="badge badge-cyan">[MCP]</span>
    <h3>Model Context Protocol</h3>
    <p>Barramento CAN DBC exposto como ferramentas nativas para LLMs inspecionarem telemetria física a 100ms.</p>
  </div>
  <div class="card">
    <span class="badge badge-amber">[RAG]</span>
    <h3>Knowledge Base</h3>
    <p>Base vetorial com esquemas elétricos, diagramas de blocos Simulink e árvores de decisão para DTCs (P0A80, P0606).</p>
  </div>
  <div class="card">
    <span class="badge badge-green">[AGENTS]</span>
    <h3>Simulink MBD</h3>
    <p>Agentes ReAct que abrem modelos, ajustam ganhos de malhas PI e executam testes MIL autônomos.</p>
  </div>
  <div class="card">
    <span class="badge badge-cyan">[FINE-TUNING]</span>
    <h3>Domain Model</h3>
    <p>Adaptação de LLMs com datasets <code>.jsonl</code> de dinâmica de motores e requisitos funcionais ISO 26262.</p>
  </div>
</div>

---

# Arquitetura do Trem de Força P2 Híbrido

A topologia **P2 Paralela** posiciona o motor elétrico (PMSM) entre a embreagem de desconexão K0 e o câmbio de dupla embreagem (e-DCT):

<div class="card">
  <code>[ICE: 1.6L Miller] === [Embreagem K0] === [PMSM 238A] === [C1/C2 e-DCT] === [Eixo de Tração]</code>
</div>

* **Modo EV Puro (K0 Aberta):** Motor elétrico traciona o veículo até 60 km/h com zero emissões e silêncio total.
* **Transição & Partida (K0 Slip/Sync):** O PMSM gira e arrasta o virabrequim do ICE até a rotação de ignição em menos de 250ms.
* **Modo P2 Hybrid Boost (K0 Trancada):** ICE no ponto ótimo de torque somado ao pico de torque elétrico ($\approx 185\text{ cv}$).
* **Frenagem Regenerativa (K0 Aberta):** O PMSM atua como gerador recarregando a bateria de alta tensão sem arrasto do motor a combustão.

---

# Arquitetura MBD: Os 4 Mains Solvers

No Simulink, o modelo é estritamente particionado para garantir determinação temporal e integridade de barramento:

<div class="grid-2">
  <div class="card">
    <h3>1. COMUNICACAO (10ms)</h3>
    <p>Gerencia Inports, buffers de entrada e decodificação de quadros CAN DBC com verificação de paridade e timeout.</p>
  </div>
  <div class="card">
    <h3>2. SOFTECU (10ms)</h3>
    <p>Executa a lógica de controle embarcada (EMS - Energy Management Strategy), controle de lambda e split de torque.</p>
  </div>
  <div class="card card-amber">
    <h3>3. MDL - PLANTA FÍSICA (1ms)</h3>
    <p>Integração contínua das equações diferenciais da admissão (MAP), inércia mecânica e dinâmica térmica.</p>
  </div>
  <div class="card">
    <h3>4. OUT - TELEMETRIA (100ms)</h3>
    <p>Condicionamento dos sensores virtuais e empacotamento dos quadros telemétricos CAN para transmissão.</p>
  </div>
</div>

---

# Ciclo Miller: Eficiência Térmica Máxima

Por que o **Ciclo Miller com EIVC** é ideal para híbridos?

<div class="grid-2">
  <div class="card">
    <h3>Termodinâmica do EIVC</h3>
    <ul>
      <li>Fechamento antecipado da válvula de admissão.</li>
      <li>Taxa de expansão ($\varepsilon_e$) maior que a compressão efetiva ($\varepsilon_{c,\text{ef}}$).</li>
      <li>Menor temperatura de combustão &rarr; Redução drástica de $\text{NO}_x$.</li>
      <li>Elimina tendência à detonação (*Knock*).</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>Sinergia com o Híbrido P2</h3>
    <ul>
      <li><strong>Desafio:</strong> Baixo torque em arrancadas.</li>
      <li><strong>Solução:</strong> O motor elétrico PMSM fornece torque instantâneo (<em>Torque Fill</em>).</li>
      <li>O ICE só é ativado quando o veículo já está em velocidade de cruzeiro e carga favorável.</li>
    </ul>
  </div>
</div>

---

# Equacionamento da Dinâmica de Admissão (MAP)

A pressão no coletor $P_m(t)$ é governada pela equação de conservação de massa:

$$\frac{dP_m}{dt} = \frac{R \cdot T_m}{V_m} \Big( \dot{m}_{ai}(t) - \dot{m}_{ao}(t) \Big)$$

<div class="grid-2">
  <div class="card">
    <strong>Entrada pela Borboleta ($\dot{m}_{ai}$):</strong>
    $$\dot{m}_{ai} = C_d A_{th}(\alpha) \frac{P_{amb}}{\sqrt{R T_{amb}}} \Psi\left(\frac{P_m}{P_{amb}}\right)$$
    Escoamento compressível isentrópico com transição sônica a $P_r \le 0.528$.
  </div>
  <div class="card">
    <strong>Bombeamento aos Cilindros ($\dot{m}_{ao}$):</strong>
    $$\dot{m}_{ao} = \frac{V_d \cdot N_e}{120 \cdot R \cdot T_m} \cdot \eta_v(N_e, P_m) \cdot P_m$$
    Abordagem <em>Speed-Density</em> dependente do rendimento volumétrico $\eta_v$.
  </div>
</div>

---

# Mapeamento BSFC & Sweet Spot (41% Eficiência)

<div class="grid-2">
  <div class="card">
    <h3>A Métrica BSFC</h3>
    $$\text{BSFC} = \frac{\dot{m}_f \text{ [g/h]}}{P_{\text{mech}} \text{ [kW]}} \quad [\text{g/kWh}]$$
    $$\eta_{th} = \frac{3600}{\text{BSFC} \cdot Q_{LHV}}$$
    Com $Q_{LHV} = 44\text{ MJ/kg}$:
    $$\text{BSFC} = 230\text{ g/kWh} \implies \mathbf{\eta_{th} = 41.0\%}$$
  </div>
  <div class="card card-amber">
    <h3>Zonas de Operação na ECU</h3>
    <ul>
      <li><span class="badge badge-green">SWEET SPOT:</span> $230 - 250\text{ g/kWh}$ (Alvo permanente do controle EMS).</li>
      <li><span class="badge badge-amber">ALTA CARGA:</span> $280 - 330\text{ g/kWh}$ (Fase de aceleração máxima).</li>
      <li><span class="badge badge-cyan">BAIXA CARGA:</span> $> 450\text{ g/kWh}$ (Evitada desligando o ICE e desacoplando K0).</li>
    </ul>
  </div>
</div>

---

# O Pilar [MCP]: Conectando Simulink com LLMs

O servidor **Model Context Protocol (JSON-RPC)** em `module_2_mcp/mcp_server.py`:

```json
// Requisição de Tool Call de um Agente Autônomo:
{
  "method": "tools/call",
  "params": {
    "name": "audit_engine_efficiency",
    "arguments": { "sample_window_s": 5.0 }
  }
}
```

```json
// Resposta Estruturada da ECU Virtual:
{
  "result": {
    "rpm_ice": 2450,
    "bsfc_g_kwh": 231.2,
    "zone": "SWEET_SPOT",
    "k0_state": "LOCKED",
    "verdict": "NOMINAL_MAX_EFFICIENCY"
  }
}
```

---

# Laboratório Prático Guiado (Hands-On Lab 1)

<div class="card">
  <strong>Objetivo:</strong> Simular um degrau de aceleração de 20% para 80% e auditar o atraso pneumático $\tau$ do coletor.
</div>

### Fluxo de Trabalho do Aluno:
1. Executar a rotina de validação analítica: `python test_pipeline.py`.
2. Acessar o **Cockpit de Telemetria** em tempo real (`http://localhost:8080`).
3. Clicar em **`SIMULADOR // EXECUTAR MIL`** para rodar a simulação com a barra de progresso sincronizada.
4. Clicar no botão dedicado **`ABRIR SIMULINK`** para inspecionar os blocos internos do modelo `MIL_MarleyOS_Powertrain.slx`.
5. Extrair o arquivo `datalogger.csv` gerado e verificar a convergência para o *Sweet Spot* BSFC.

---

# Resumo do Módulo 1 & Próximos Passos

<div class="grid-2">
  <div class="card">
    <h3>O que Dominamos Hoje</h3>
    <ul>
      <li>Termodinâmica do Ciclo Miller com EIVC.</li>
      <li>Equações diferenciais de Speed-Density para o MAP.</li>
      <li>Cálculo analítico do BSFC e rendimento de 41%.</li>
      <li>Segregação dos 4 Solvers MBD em Simulink.</li>
      <li>Protocolo MCP expondo telemetria CAN a LLMs.</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>Próximo Módulo (Módulo 2)</h3>
    <ul>
      <li><strong>Tração Elétrica & FOC (BEV):</strong></li>
      <li>Motor Síncrono de Ímãs Permanentes (PMSM).</li>
      <li>Transformadas de Clarke e Park ($abc \to \alpha\beta \to dq$).</li>
      <li>Controle por Orientação de Campo (FOC) com malhas PI de corrente $I_d$ e $I_q$.</li>
    </ul>
  </div>
</div>

---

<!-- _class: lead -->

# NEXUSMBD // FIM DO MÓDULO 1
### Dúvidas Técnicas & Discussão de Arquitetura

<div style="margin-top: 20px;">
  <code>Repositório: https://github.com/marleyrosa/MarleyOS.git</code><br>
  <code>Cockpit Local: http://localhost:8080 | Wi-Fi: http://192.168.1.22:8080</code>
</div>
