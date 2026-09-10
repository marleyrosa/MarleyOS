---
marp: true
theme: nexusmbd
paginate: true
header: "NexusMBD // AI-Native Powertrain Suite"
footer: "Módulos 2 & 3: Eletrificação BEV & Híbrido Paralelo P2"
size: 16:9
---

<!-- _class: lead -->

# NEXUSMBD // ELETRICAÇÃO & HEV
### Módulos 2 & 3: Tração Elétrica PMSM, FOC & Híbrido P2
Controle Vetorial • Embreagem K0 • Câmbio e-DCT • Transição Dinâmica

<div style="margin-top: 25px;">
  <span class="badge badge-cyan">PMSM 238A</span>
  <span class="badge badge-green">FOC Id/Iq</span>
  <span class="badge badge-amber">Embreagem K0</span>
  <span class="badge badge-cyan">e-DCT 6-Speed</span>
</div>

---

# Motor Síncrono de Ímãs Permanentes (PMSM)

A máquina de tração elétrica do NexusMBD opera sob o princípio do campo girante estatórico sincronizado com os ímãs de neodímio do rotor:

<div class="grid-2">
  <div class="card">
    <h3>Parâmetros da Máquina</h3>
    <ul>
      <li><strong>Tensão Barramento DC:</strong> $350\text{ V}$</li>
      <li><strong>Corrente Nominal:</strong> $200\text{ A}_{rms}$ (Pico: $238.5\text{ A}$)</li>
      <li><strong>Pares de Polos ($p$):</strong> 4 (8 polos)</li>
      <li><strong>Fluxo dos Ímãs ($\psi_{pm}$):</strong> $0.082\text{ Wb}$</li>
      <li><strong>Frequência Máxima:</strong> $311\text{ Hz}$ ($4665\text{ RPM}$)</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>Produção de Torque ($dq$)</h3>
    $$T_{em} = \frac{3}{2} p \Big( \psi_{pm} i_q + (L_d - L_q) i_d i_q \Big)$$
    <ul>
      <li><strong>Torque de Ímã:</strong> proporcional à corrente de quadratura ($I_q$).</li>
      <li><strong>Torque de Relutância:</strong> aproveitado com $I_d < 0$ via controle MTPA (*Maximum Torque Per Ampere*).</li>
    </ul>
  </div>
</div>

---

# Controle Vetorial FOC (Field-Oriented Control)

O FOC transforma correntes alternadas senoidais em grandezas de corrente contínua desacopladas:

<div class="card">
  <code>[Correntes ia, ib, ic] ==(Clarke)==> [iα, iβ] ==(Park θe)==> [id (Fluxo), iq (Torque)]</code>
</div>

<div class="grid-2">
  <div class="card">
    <h3>Eixo Direto ($I_d$) &mdash; Fluxo</h3>
    <ul>
      <li>Alinhado com o vetor de campo do ímã.</li>
      <li>Mantido em $I_d = 0$ em baixas rotações para máxima eficiência por ampere.</li>
      <li>Injetado negativo ($I_d < 0$) para <strong>Enfraquecimento de Campo</strong> em alta rotação.</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>Eixo em Quadratura ($I_q$) &mdash; Torque</h3>
    <ul>
      <li>Ortogonal ao fluxo magnético ($90^\circ$ elétricos).</li>
      <li>Controla diretamente o torque de aceleração do veículo.</li>
      <li>Regulador PI com desacoplamento da Back-EMF $\omega_e \psi_{pm}$.</li>
    </ul>
  </div>
</div>

---

# Arquitetura do Híbrido Paralelo P2

A topologia **P2** posiciona o motor elétrico entre a embreagem de desconexão K0 e o câmbio:

<div class="card">
  <code>[ICE: 1.6L Miller] === [Embreagem K0] === [PMSM 238A] === [e-DCT] === [Rodas]</code>
</div>

<div class="grid-2">
  <div class="card">
    <h3>Vantagens Estruturais</h3>
    <ul>
      <li><strong>Modo EV Puro:</strong> K0 aberta elimina 100% do arrasto de atrito do motor térmico na cidade.</li>
      <li><strong>Regeneração Plena:</strong> PMSM desacoplado do ICE recupera até $45\text{ kW}$ de energia cinética na frenagem.</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>Desafio Dinâmico</h3>
    <ul>
      <li><strong>Partida a Quente em Movimento:</strong> A embreagem K0 deve escorregar, arrastar o ICE de 0 a 2500 RPM e acoplar sem tranco no passageiro ($< 0.05\text{ G}$).</li>
    </ul>
  </div>
</div>

---

# Máquina de Estados da Embreagem K0

O supervisor eletro-hidráulico comanda 4 estados finitos:

<div class="grid-4">
  <div class="card">
    <span class="badge badge-cyan">1. OPEN</span>
    <h3>Modo EV Puro</h3>
    <p>$P_{k0} = 0\text{ bar}$.<br>ICE desligado.<br>PMSM traciona o veículo silenciosamente.</p>
  </div>
  <div class="card">
    <span class="badge badge-amber">2. SYNC</span>
    <h3>Pre-Fill Hidráulico</h3>
    <p>$0 < P_{k0} < 2\text{ bar}$.<br>Eliminação de folga das lamelas de fricção.</p>
  </div>
  <div class="card">
    <span class="badge badge-amber">3. SLIP</span>
    <h3>Escorregamento</h3>
    <p>$P_{k0} \approx 6\text{ bar}$.<br>Torque de arraste controlado via PMSM (Torque Fill).</p>
  </div>
  <div class="card">
    <span class="badge badge-green">4. LOCKED</span>
    <h3>Acoplamento Pleno</h3>
    <p>$P_{k0} \ge 14\text{ bar}$.<br>$\Delta\omega = 0$.<br>P2 Hybrid Boost ativo ($185\text{ cv}$).</p>
  </div>
</div>

---

# Transmissão e-DCT & Estratégia EMS

<div class="grid-2">
  <div class="card">
    <h3>Transmissão e-DCT</h3>
    <ul>
      <li><strong>Embreagem C1:</strong> Marchas 1, 3 e 5.</li>
      <li><strong>Embreagem C2:</strong> Marchas 2, 4, 6 e Ré.</li>
      <li><strong>Power Shift:</strong> Pré-seleção mecânica e cruzamento progressivo de pressões de óleo sem queda de aceleração.</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>Estratégia EMS (Torque Split)</h3>
    <ul>
      <li><strong>Load Point Moving:</strong> O ICE é forçado a operar em seu *Sweet Spot* BSFC ($140\text{ N}\cdot\text{m}$).</li>
      <li>O excedente de torque aciona o PMSM como gerador, recarregando a bateria HV sem queimar combustível a mais.</li>
    </ul>
  </div>
</div>

---

<!-- _class: lead -->

# NEXUSMBD // FIM DOS MÓDULOS 2 & 3
### Próximo Passo: Os 4 Pilares de Inteligência Artificial

<div style="margin-top: 20px;">
  <code>Cockpit Local: http://localhost:8080 | Apostila: http://localhost:8080/apostila</code>
</div>
