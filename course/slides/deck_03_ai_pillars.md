---
marp: true
theme: nexusmbd
paginate: true
header: "NexusMBD // AI-Native Powertrain Suite"
footer: "Módulos 4 a 8: Os 4 Pilares de IA, Capstone & Certificação"
size: 16:9
---

<!-- _class: lead -->

# NEXUSMBD // OS 4 PILARES DE IA
### Módulos 4 ao 8: Arquitetura de IA Aplicada & Certificação
[MCP] Servidor • [RAG] Fontes • [AGENTS] Simulink • [FINE-TUNING] ISO 26262

<div style="margin-top: 25px;">
  <span class="badge badge-cyan">[MCP] Tool Server</span>
  <span class="badge badge-amber">[RAG] Hybrid Search</span>
  <span class="badge badge-green">[AGENTS] ReAct MIL</span>
  <span class="badge badge-cyan">[FINE-TUNING] ASIL-D</span>
</div>

---

# Pilar 1: [MCP] Model Context Protocol

<div class="card">
  <strong>O que o aluno constrói:</strong> Um servidor MCP JSON-RPC em Python que transforma o barramento veicular CAN DBC em ferramentas cognitivas nativas para LLMs.
</div>

<div class="grid-2">
  <div class="card">
    <h3>Parser CAN DBC Nativo</h3>
    <ul>
      <li>Decodifica frames industriais <code>.dbc</code>.</li>
      <li>Mapeia little-endian (Intel) e big-endian.</li>
      <li>Aplica fatores de escala e limites físicos em tempo real.</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>Ferramentas no Servidor (*Tools*)</h3>
    <ul>
      <li><code>read_can_telemetry</code>: streaming contínuo de 18 canais a 100ms.</li>
      <li><code>inject_fault_code</code>: injeção de falhas para auditoria.</li>
      <li><code>set_k0_pressure</code>: calibração remota via IA.</li>
    </ul>
  </div>
</div>

---

# Pilar 2: [RAG] Conectando Boas Fontes de Engenharia

<div class="card">
  <strong>O que o aluno constrói:</strong> Uma pipeline de busca híbrida especializada em powertrain e árvores de decisão para códigos DTC.
</div>

<div class="grid-2">
  <div class="card">
    <h3>Busca Híbrida (Hybrid Search)</h3>
    <ul>
      <li><strong>Embeddings Densos:</strong> Similaridade semântica para conceitos físicos.</li>
      <li><strong>BM25 Esparso:</strong> Correspondência literal exata para códigos de peças e identificadores CAN.</li>
      <li>Fusão de ranking via <strong>Reciprocal Rank Fusion (RRF)</strong>.</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>Isolamento de DTCs Críticos</h3>
    <ul>
      <li><code>P0A80</code>: Degradação de bateria HV.</li>
      <li><code>P0606</code>: Falha de watchdog na CPU da ECU.</li>
      <li><code>C0035</code>: Sensor de velocidade de roda.</li>
      <li><code>P0AA6</code>: Perda de isolamento galvânico ($500 \ \Omega/\text{V}$).</li>
    </ul>
  </div>
</div>

---

# Pilar 3: [AGENTS] Criando um Agente para o Simulink

<div class="card">
  <strong>O que o aluno constrói:</strong> Um Agente ReAct autônomo em Python que opera o MATLAB/Simulink sem intervenção humana.
</div>

<div class="grid-2">
  <div class="card">
    <h3>O Loop Cognitivo ReAct</h3>
    <ul>
      <li><strong>Thought:</strong> Analisa a meta e formula a hipótese de ganhos.</li>
      <li><strong>Action:</strong> Dispara simulação com <code>Simulink.SimulationInput</code>.</li>
      <li><strong>Observation:</strong> Extrai sinais <code>logsout</code> e calcula ITAE.</li>
      <li><strong>Reflection:</strong> Itera os ganhos até atingir a especificação.</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>Calibração em Malha Fechada</h3>
    <ul>
      <li>Otimiza ganhos de corrente $K_p, K_i$ do inversor PMSM.</li>
      <li>Convergência garantida em menos de 8 rodadas.</li>
      <li>Reduz o overshoot de torque para $< 5\%$.</li>
    </ul>
  </div>
</div>

---

# Pilar 4: [FINE-TUNING] Adaptação para Domínio Automotivo

<div class="card">
  <strong>O que o aluno constrói:</strong> Um modelo de linguagem adaptado (LoRA/QLoRA) alinhado com a norma de segurança funcional **ISO 26262 (ASIL-D)**.
</div>

<div class="grid-2">
  <div class="card">
    <h3>Engenharia de Datasets</h3>
    <ul>
      <li>Geração sintética de telemetria em <code>.jsonl</code>.</li>
      <li>Pares instrução-resposta 100% fundamentados em física (zero alucinações).</li>
      <li>Adaptação leve com matrizes de baixa ordem ($r=16, \alpha=32$).</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>Conformidade ASIL-D (HARA)</h3>
    <ul>
      <li>Severidade ($S3$), Exposição ($E4$), Controlabilidade ($C3$).</li>
      <li>Auditoria contínua de metas de segurança (*Safety Goals*).</li>
      <li>Validação contra falhas de aceleração inadvertida.</li>
    </ul>
  </div>
</div>

---

# Sistema de Avaliação & Certificação (1.000 Pontos)

Para obter o certificado **NexusMBD Certified Powertrain AI Architect**:

<div class="grid-2">
  <div class="card">
    <h3>Distribuição de Pontos</h3>
    <ul>
      <li><strong>Módulos 1 a 7:</strong> 100 pontos cada (700 pts)</li>
      <li><strong>Módulo 8 (Capstone & Exame):</strong> 300 pontos</li>
      <li><strong>Total Geral:</strong> 1.000 pontos</li>
      <li><strong>Nota Mínima de Aprovação:</strong> $\ge 700\text{ pts}$ ($70\%$)</li>
    </ul>
  </div>
  <div class="card card-amber">
    <h3>Certificado Digital Autenticado</h3>
    <ul>
      <li>Hash criptográfico SHA-256 anti-fraude.</li>
      <li>Selo de conformidade técnica ISO 26262.</li>
      <li>Emissão automatizada via <code>evaluate_course.py</code>.</li>
      <li>Distinções de Honra e Excelência (*Summa Cum Laude*).</li>
    </ul>
  </div>
</div>

---

<!-- _class: lead -->

# NEXUSMBD // FORMAÇÃO CONCLUÍDA
### Validação Prática & Exame Final no Cockpit

<div style="margin-top: 20px;">
  <code>Executar Avaliação: python course/certification/evaluate_course.py</code><br>
  <code>Cockpit: http://localhost:8080 | Apostila: http://localhost:8080/apostila</code>
</div>
