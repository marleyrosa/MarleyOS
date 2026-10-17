"use client";

import React, { useEffect, useRef } from "react";
import { ManuscriptState } from "@/data/orbital-lab/manuscript";
import { Gauge, CheckCircle, TrendingUp, AlertTriangle } from "lucide-react";

interface PanelMetricsProps {
  manuscript: ManuscriptState;
  swarmActive: boolean;
}

export function PanelMetrics({ manuscript, swarmActive }: PanelMetricsProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;
    let offset = 0;

    const render = () => {
      animId = requestAnimationFrame(render);
      offset += swarmActive ? 0.08 : 0.03;

      const w = canvas.width;
      const h = canvas.height;

      // Dark background
      ctx.fillStyle = "#050912";
      ctx.fillRect(0, 0, w, h);

      // Baseline reference (zero error)
      const centerY = h * 0.5;
      ctx.strokeStyle = "rgba(100, 116, 139, 0.25)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, centerY);
      ctx.lineTo(w, centerY);
      ctx.stroke();

      // Error tolerance band (+- 0.1 A)
      const bandHeight = 16;
      ctx.fillStyle = "rgba(16, 185, 129, 0.05)";
      ctx.fillRect(0, centerY - bandHeight, w, bandHeight * 2);

      // Wave 1: Bench Current actual vs estimated
      ctx.beginPath();
      ctx.strokeStyle = "#10b981"; // emerald for HIL measurement
      ctx.lineWidth = 1.5;

      const points = 160;
      for (let i = 0; i < points; i++) {
        const x = (i / points) * w;
        // high frequency ripple from PWM switching (20kHz simulation)
        const fundamental = Math.sin((i * 0.06) + offset);
        const harmonic = 0.15 * Math.sin((i * 0.24) - offset * 2);
        const noise = (Math.random() - 0.5) * 1.5;
        const errorVal = (fundamental * 6 + harmonic * 4 + noise);
        const y = centerY + errorVal;

        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      // Confidence dots
      ctx.fillStyle = "#34d399";
      for (let i = 10; i < points; i += 25) {
        const x = (i / points) * w;
        const fundamental = Math.sin((i * 0.06) + offset);
        const y = centerY + fundamental * 6;
        ctx.beginPath();
        ctx.arc(x, y, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }
    };

    render();

    return () => cancelAnimationFrame(animId);
  }, [swarmActive]);

  const { hilBenchmarks } = manuscript;

  return (
    <div className="flex flex-col h-full bg-[#070b14] border border-cyan-950/70 rounded-lg p-3 text-xs font-mono text-zinc-300 shadow-inner overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-cyan-900/40 pb-2 mb-2">
        <div className="flex items-center gap-1.5 text-cyan-400 font-bold tracking-wider">
          <Gauge className="w-3.5 h-3.5 text-emerald-400" />
          <span>[04] VALIDATION // SAMPLE METRICS</span>
        </div>
        <span className="text-[10px] text-emerald-400 flex items-center gap-1 font-semibold">
          <CheckCircle className="w-3 h-3" /> HIL VERIFIED
        </span>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-3 gap-1.5 mb-2">
        <div className="bg-zinc-900/80 border border-zinc-800 rounded p-1.5 text-center">
          <div className="text-[9px] text-zinc-500">RMSE ERROR</div>
          <div className="text-emerald-300 font-bold text-xs">{hilBenchmarks.rmseErrorPercent}%</div>
        </div>
        <div className="bg-zinc-900/80 border border-zinc-800 rounded p-1.5 text-center">
          <div className="text-[9px] text-zinc-500">MAX JITTER</div>
          <div className="text-cyan-300 font-bold text-xs">{hilBenchmarks.maxJitterMicroseconds} us</div>
        </div>
        <div className="bg-zinc-900/80 border border-zinc-800 rounded p-1.5 text-center">
          <div className="text-[9px] text-zinc-500">CORRELATION</div>
          <div className="text-violet-300 font-bold text-xs">{(hilBenchmarks.correlationFactor * 100).toFixed(1)}%</div>
        </div>
      </div>

      {/* Real-time Residual Error Oscilloscope */}
      <div className="relative w-full h-24 bg-[#050912] border border-cyan-900/40 rounded overflow-hidden mb-1.5">
        <canvas ref={canvasRef} width={340} height={96} className="w-full h-full block" />
        <div className="absolute top-1 left-2 text-[9px] text-emerald-400/90 font-mono">
          RESIDUAL e(t) = |i_bench - i_sim|
        </div>
        <div className="absolute bottom-1 right-2 text-[9px] text-zinc-500 font-mono">
          BAND: &plusmn;0.05% RMSE
        </div>
      </div>

      <div className="flex items-center justify-between text-[9.5px] text-zinc-400 pt-0.5">
        <span>BENCH: {hilBenchmarks.platform}</span>
        <span className="text-cyan-400 font-mono">FS = {hilBenchmarks.samplingRateKhz} kHz</span>
      </div>
    </div>
  );
}
