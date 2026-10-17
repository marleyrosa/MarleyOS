export interface SwarmAgent {
  id: "AG-01" | "AG-02" | "AG-03" | "AG-04" | "AG-05";
  name: string;
  role: string;
  operationalFunction: string;
  inputFormat: string;
  outputFormat: string;
  status: "ONLINE" | "COMPUTING" | "SYNCING" | "IDLE";
  progress: number; // 0 - 100%
  cycleCount: number;
  lastExecutionMs: number;
  cpuLoadPercent: number;
  badgeColor: string;
  currentTask: string;
  recentLogs: string[];
}

export const INITIAL_SWARM_AGENTS: SwarmAgent[] = [
  {
    id: "AG-01",
    name: "Paper Parser & Extractor",
    role: "Ingestion & AST Extraction",
    operationalFunction: "Lê rascunhos, equações, modelos Simulink/Python e tabelas do artigo central.",
    inputFormat: "LaTeX / Draft / Notebook Kiotopaper",
    outputFormat: "Nós semânticos, equações LaTeX e blocos executáveis",
    status: "ONLINE",
    progress: 100,
    cycleCount: 148,
    lastExecutionMs: 14,
    cpuLoadPercent: 12,
    badgeColor: "#06b6d4", // cyan
    currentTask: "Listening for manuscript AST node updates...",
    recentLogs: [
      "[00:02:11] Extracted 28 LaTeX equations from Sec 2, 3, 4.",
      "[00:02:14] Serialized 7 structured sections into AST graph.",
      "[00:02:18] Verified Python EKF implementation consistency.",
    ],
  },
  {
    id: "AG-02",
    name: "XIL & HIL Validator",
    role: "Hardware-in-the-Loop Verification",
    operationalFunction: "Valida integridade e consistência dos dados de ensaio (MIL, SIL, HIL dSPACE/ETAS).",
    inputFormat: "Logs de bancada HIL / CSV de telemetria",
    outputFormat: "Curvas de dispersão, RMSE (0.042%) e métricas de fidelidade",
    status: "COMPUTING",
    progress: 92,
    cycleCount: 204,
    lastExecutionMs: 38,
    cpuLoadPercent: 48,
    badgeColor: "#10b981", // emerald
    currentTask: "Computing covariance dispersion on 20 kHz SCALEXIO stream...",
    recentLogs: [
      "[00:02:12] Bench correlation evaluated: r = 0.9942.",
      "[00:02:15] Jitter threshold verification: max 0.85 us (PASS).",
      "[00:02:19] Re-evaluating Lyapunov candidate convergence.",
    ],
  },
  {
    id: "AG-03",
    name: "Editorial Scope Matcher",
    role: "Journal Adherence Scorer",
    operationalFunction: "Compara densidade técnica com escopos dos 10 periódicos (IEEE TTE vs CEP vs SAE).",
    inputFormat: "Conteúdo do artigo & equações",
    outputFormat: "Score de Aderência (0 a 100%) por periódico",
    status: "SYNCING",
    progress: 88,
    cycleCount: 96,
    lastExecutionMs: 22,
    cpuLoadPercent: 29,
    badgeColor: "#8b5cf6", // violet
    currentTask: "Cross-matching IEEE TTE requirements vs Els CEP...",
    recentLogs: [
      "[00:02:08] IEEE TTE scored at 96% fit (optimal match).",
      "[00:02:13] Elsevier CEP scored at 92% (strong HIL match).",
      "[00:02:17] SAE WCX flagged for 34-day critical deadline.",
    ],
  },
  {
    id: "AG-04",
    name: "Deadline & Timeline Tracker",
    role: "Submission Schedule Tracker",
    operationalFunction: "Monitora chamadas abertas, datas de abstract, encerramento de submissão e tempo de revisão.",
    inputFormat: "Calendários orbitais e chamadas de papers",
    outputFormat: "Linhas temporais críticas de submissão e regressões",
    status: "ONLINE",
    progress: 100,
    cycleCount: 65,
    lastExecutionMs: 8,
    cpuLoadPercent: 7,
    badgeColor: "#f59e0b", // amber
    currentTask: "Tracking 10 orbital submission horizons...",
    recentLogs: [
      "[00:02:05] IFAC 2026: 21 days remaining to close.",
      "[00:02:10] SAE Brasil: 28 days remaining.",
      "[00:02:16] SAE WCX 2027: 34 days remaining.",
    ],
  },
  {
    id: "AG-05",
    name: "Cost & Compliance Auditor",
    role: "Budget & Template Auditor",
    operationalFunction: "Calcula custos de APC (Open Access vs Subscrição), excesso de páginas e templates.",
    inputFormat: "Extensão do paper / Financiamento",
    outputFormat: "Orçamento estimado (USD/EUR/BRL) e alertas de formatação",
    status: "ONLINE",
    progress: 95,
    cycleCount: 112,
    lastExecutionMs: 16,
    cpuLoadPercent: 15,
    badgeColor: "#ec4899", // pink
    currentTask: "Auditing page charges for 2-column IEEE format...",
    recentLogs: [
      "[00:02:03] Page count estimated: 9 pages (No excess fee in IEEE).",
      "[00:02:09] Converted APC estimate: USD 2,495 / BRL 13,720.",
      "[00:02:15] Subscription model available: zero direct author fee.",
    ],
  },
];
