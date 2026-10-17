"use client";

import React, { useEffect, useRef, useState } from "react";
import { Activity, Play, RefreshCw, Zap } from "lucide-react";

interface PanelSimulationProps {
  swarmActive: boolean;
}

export function PanelSimulation({ swarmActive }: PanelSimulationProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stepCurrent, setStepCurrent] = useState<number>(65); // Amperes
  const [dampingFactor, setDampingFactor] = useState<number>(0.707); // Zeta
  const [settlingTimeMs, setSettlingTimeMs] = useState<number>(4.2);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;
    let t = 0;

    const render = () => {
      animId = requestAnimationFrame(render);
      t += swarmActive ? 0.05 : 0.025;

      const w = canvas.width;
      const h = canvas.height;

      // Dark oscilloscope background
      ctx.fillStyle = "#050912";
      ctx.fillRect(0, 0, w, h);

      // Grid lines
      ctx.strokeStyle = "rgba(6, 182, 212, 0.08)";
      ctx.lineWidth = 1;
      const gridStep = 24;
      for (let x = 0; x < w; x += gridStep) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
      }
      for (let y = 0; y < h; y += gridStep) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }

      // Zero baseline & target setpoint
      const centerY = h * 0.72;
      const targetY = centerY - (stepCurrent / 100) * (h * 0.5);

      ctx.strokeStyle = "rgba(245, 158, 11, 0.45)"; // amber setpoint line
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(0, targetY);
      ctx.lineTo(w, targetY);
      ctx.stroke();
      ctx.setLineDash([]);

      // Draw transient response wave: y(tau) = 1 - e^(-zeta*wn*tau) * (cos(wd*tau) + ...)
      ctx.beginPath();
      ctx.lineWidth = 2;
      ctx.strokeStyle = "#06b6d4"; // cyan response curve

      const pointsCount = w;
      const wn = 14.0;
      const zeta = dampingFactor;
      const wd = wn * Math.sqrt(Math.max(0.01, 1 - zeta * zeta));

      for (let i = 0; i < pointsCount; i++) {
        const tau = (i / pointsCount) * 1.5;
        const decay = Math.exp(-zeta * wn * tau);
        const osc = Math.cos(wd * tau + t * 0.5) + (zeta / Math.sqrt(1 - zeta * zeta)) * Math.sin(wd * tau + t * 0.5);
        const yVal = 1 - decay * osc;
        const screenY = centerY - yVal * (centerY - targetY);

        if (i === 0) ctx.moveTo(i, screenY);
        else ctx.lineTo(i, screenY);
      }
      ctx.stroke();

      // Glowing tip photon
      const tipIndex = (Math.floor(t * 40) % pointsCount);
      const tipTau = (tipIndex / pointsCount) * 1.5;
      const tipDecay = Math.exp(-zeta * wn * tipTau);
      const tipOsc = Math.cos(wd * tipTau + t * 0.5) + (zeta / Math.sqrt(1 - zeta * zeta)) * Math.sin(wd * tipTau + t * 0.5);
      const tipScreenY = centerY - (1 - tipDecay * tipOsc) * (centerY - targetY);

      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(tipIndex, tipScreenY, 3, 0, Math.PI * 2);
      ctx.fill();

      // Shadow / glow below curve
      ctx.lineTo(w, h);
      ctx.lineTo(0, h);
      ctx.closePath();
      const grad = ctx.createLinearGradient(0, targetY, 0, h);
      grad.addColorStop(0, "rgba(6, 182, 212, 0.15)");
      grad.addColorStop(1, "rgba(6, 182, 212, 0.0)");
      ctx.fillStyle = grad;
      ctx.fill();
    };

    render();

    return () => cancelAnimationFrame(animId);
  }, [stepCurrent, dampingFactor, swarmActive]);

  return (
    <div className="flex flex-col h-full bg-[#070b14] border border-cyan-950/70 rounded-lg p-3 text-xs font-mono text-zinc-300 shadow-inner overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-cyan-900/40 pb-2 mb-2">
        <div className="flex items-center gap-1.5 text-cyan-400 font-bold tracking-wider">
          <Activity className="w-3.5 h-3.5 text-emerald-400" />
          <span>[02] PARTICLE / SIMULATION SOLVER</span>
        </div>
        <span className="text-[10px] text-zinc-400">
          PMSM $i_q$ TRANSIENT (20 kHz)
        </span>
      </div>

      {/* Mini Oscilloscope Canvas */}
      <div className="relative w-full h-28 bg-[#050912] border border-cyan-900/40 rounded overflow-hidden mb-2">
        <canvas ref={canvasRef} width={340} height={112} className="w-full h-full block" />
        <div className="absolute top-1 left-2 text-[9px] text-cyan-400/80 font-mono">
          $i_q^*(t)$ = {stepCurrent} A | $\zeta$ = {dampingFactor} | $t_s$ = {settlingTimeMs} ms
        </div>
        <div className="absolute bottom-1 right-2 text-[9px] text-amber-400/90 font-mono">
          SETPOINT TARGET
        </div>
      </div>

      {/* Parameter Sliders */}
      <div className="grid grid-cols-2 gap-2 text-[10px]">
        <div>
          <div className="flex justify-between text-zinc-400 mb-0.5">
            <span>INVERTER CURRENT ($i_q^*$)</span>
            <span className="text-cyan-300 font-bold">{stepCurrent} A</span>
          </div>
          <input
            type="range"
            min="20"
            max="120"
            value={stepCurrent}
            onChange={(e) => setStepCurrent(Number(e.target.value))}
            className="w-full h-1 bg-zinc-800 rounded appearance-none cursor-pointer accent-cyan-400"
          />
        </div>
        <div>
          <div className="flex justify-between text-zinc-400 mb-0.5">
            <span>DAMPING RATIO ($\zeta$)</span>
            <span className="text-emerald-300 font-bold">{dampingFactor}</span>
          </div>
          <input
            type="range"
            min="0.3"
            max="1.0"
            step="0.05"
            value={dampingFactor}
            onChange={(e) => {
              const z = Number(e.target.value);
              setDampingFactor(z);
              setSettlingTimeMs(Number((4.0 / (z * 1.2)).toFixed(1)));
            }}
            className="w-full h-1 bg-zinc-800 rounded appearance-none cursor-pointer accent-emerald-400"
          />
        </div>
      </div>
    </div>
  );
}
