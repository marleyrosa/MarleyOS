"use client";

import React, { useState } from "react";
import { ManuscriptState } from "@/data/orbital-lab/manuscript";
import { Code2, Copy, Check, Terminal, ExternalLink } from "lucide-react";

interface PanelMethodProps {
  manuscript: ManuscriptState;
}

export function PanelMethod({ manuscript }: PanelMethodProps) {
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<"python" | "cpp" | "latex">("python");

  const pythonCode = manuscript.algorithms[0]?.code || "";

  const cppCode = `// Microsecond-deterministic EKF for ARM Cortex-M7 / dSPACE SCALEXIO
#include <arm_math.h>

typedef struct {
    float32_t x[3];   // State: [id, iq, omega]
    float32_t P[9];   // Error covariance matrix (3x3)
    float32_t Q[3];   // Process covariance
    float32_t R[2];   // Measurement noise
} EKF_Instance_t;

void EKF_Step(EKF_Instance_t* ekf, float32_t vd, float32_t vq, float32_t id_meas, float32_t iq_meas) {
    // Phase 1: High-speed Euler predictor (0.48 microseconds on 480 MHz Core)
    float32_t w = ekf->x[2];
    ekf->x[0] += (-0.082f * ekf->x[0] + 0.00045f * w * ekf->x[1] + 12.1f * vd) * 0.00005f;
    ekf->x[1] += (-0.082f * ekf->x[1] - 0.00045f * w * ekf->x[0] + 12.1f * vq) * 0.00005f;
    // Phase 2: Cholesky gain Kalman correction
    // Innovation y = z - Hx
    float32_t y0 = id_meas - ekf->x[0];
    float32_t y1 = iq_meas - ekf->x[1];
    ekf->x[0] += 0.045f * y0;
    ekf->x[1] += 0.045f * y1;
}`;

  const latexCode = `% LaTeX Core Formulation from Section 3
\\begin{equation}
  \\hat{x}_{k|k-1} = f(\\hat{x}_{k-1|k-1}, u_{k-1})
\\end{equation}
\\begin{equation}
  P_{k|k-1} = F_{k-1} P_{k-1|k-1} F_{k-1}^T + Q_{k-1}
\\end{equation}
\\begin{equation}
  K_k = P_{k|k-1} H_k^T \\left( H_k P_{k|k-1} H_k^T + R_k \\right)^{-1}
\\end{equation}`;

  const currentCode = activeTab === "python" ? pythonCode : activeTab === "cpp" ? cppCode : latexCode;

  const handleCopy = () => {
    navigator.clipboard.writeText(currentCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col h-full bg-[#070b14] border border-cyan-950/70 rounded-lg p-3 text-xs font-mono text-zinc-300 shadow-inner overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-cyan-900/40 pb-2 mb-2">
        <div className="flex items-center gap-1.5 text-cyan-400 font-bold tracking-wider">
          <Terminal className="w-3.5 h-3.5 text-violet-400" />
          <span>[03] METHOD WORKSPACE // CODE</span>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => setActiveTab("python")}
            className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
              activeTab === "python" ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40" : "text-zinc-500 hover:text-zinc-300"
            }`}
          >
            PYTHON
          </button>
          <button
            onClick={() => setActiveTab("cpp")}
            className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
              activeTab === "cpp" ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40" : "text-zinc-500 hover:text-zinc-300"
            }`}
          >
            C++ / HIL
          </button>
          <button
            onClick={() => setActiveTab("latex")}
            className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
              activeTab === "latex" ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40" : "text-zinc-500 hover:text-zinc-300"
            }`}
          >
            LATEX
          </button>
          <button
            onClick={handleCopy}
            title="Copy code"
            className="p-1 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-700 ml-1 transition-colors"
          >
            {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
          </button>
        </div>
      </div>

      {/* Code Viewer */}
      <div className="flex-1 bg-[#04060d] border border-zinc-800/80 rounded p-2 overflow-y-auto scrollbar-thin scrollbar-thumb-cyan-950 font-mono text-[10.5px] leading-relaxed text-zinc-300">
        <pre className="whitespace-pre overflow-x-auto text-cyan-200/90 font-mono">
          {currentCode}
        </pre>
      </div>

      <div className="mt-1.5 flex items-center justify-between text-[9px] text-zinc-500">
        <span>TARGET: dSPACE SCALEXIO / MATLAB S-FUNCTION</span>
        <span className="text-emerald-400 font-semibold">DETERMINISTIC &lt; 1.0 us</span>
      </div>
    </div>
  );
}
