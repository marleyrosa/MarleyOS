"use client";

import React from "react";
import { SwarmAgent } from "@/data/orbital-lab/agents";
import { Users, Play, Pause, FastForward, Cpu, CheckCircle2 } from "lucide-react";

interface PanelAgentsProps {
  agents: SwarmAgent[];
  swarmActive: boolean;
  onToggleSwarm: () => void;
  onStepSwarm: () => void;
  selectedAgentId: string | null;
  onSelectAgent: (agentId: string) => void;
}

export function PanelAgents({
  agents,
  swarmActive,
  onToggleSwarm,
  onStepSwarm,
  selectedAgentId,
  onSelectAgent,
}: PanelAgentsProps) {
  return (
    <div className="flex flex-col h-full bg-[#070b14] border border-cyan-950/70 rounded-lg p-3 text-xs font-mono text-zinc-300 shadow-inner overflow-hidden">
      {/* Header with Dispatch Controls */}
      <div className="flex items-center justify-between border-b border-cyan-900/40 pb-2 mb-2">
        <div className="flex items-center gap-1.5 text-cyan-400 font-bold tracking-wider">
          <Users className="w-3.5 h-3.5 text-cyan-400" />
          <span>[05] AGENT DISPATCH // SWARM</span>
        </div>
        <div className="flex items-center gap-1.5">
          <button
            onClick={onStepSwarm}
            title="Step Cycle"
            className="flex items-center gap-1 px-1.5 py-0.5 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-700 text-[10px] transition-colors"
          >
            <FastForward className="w-2.5 h-2.5" /> STEP
          </button>
          <button
            onClick={onToggleSwarm}
            className={`flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold transition-all ${
              swarmActive
                ? "bg-amber-500/20 text-amber-300 border border-amber-500/50 shadow-[0_0_8px_rgba(245,158,11,0.25)]"
                : "bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 hover:bg-emerald-500/30"
            }`}
          >
            {swarmActive ? (
              <>
                <Pause className="w-2.5 h-2.5" /> RUNNING
              </>
            ) : (
              <>
                <Play className="w-2.5 h-2.5" /> DISPATCH
              </>
            )}
          </button>
        </div>
      </div>

      {/* Agents List */}
      <div className="flex-1 overflow-y-auto space-y-1.5 pr-1 scrollbar-thin scrollbar-thumb-cyan-950 text-[11px]">
        {agents.map((ag) => {
          const isSelected = selectedAgentId === ag.id;
          return (
            <div
              key={ag.id}
              onClick={() => onSelectAgent(ag.id)}
              className={`p-2 rounded cursor-pointer transition-all border ${
                isSelected
                  ? "bg-cyan-950/40 border-cyan-500/80 shadow-[0_0_12px_rgba(6,182,212,0.15)]"
                  : "bg-zinc-950/70 border-zinc-800/80 hover:border-cyan-800/60"
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span
                    className="px-1.5 py-0.2 rounded font-bold text-[10px]"
                    style={{ backgroundColor: `${ag.badgeColor}22`, color: ag.badgeColor, border: `1px solid ${ag.badgeColor}55` }}
                  >
                    {ag.id}
                  </span>
                  <span className="font-semibold text-zinc-100">{ag.name}</span>
                </div>
                <div className="flex items-center gap-2 text-[10px]">
                  <span
                    className={`font-semibold ${
                      ag.status === "COMPUTING"
                        ? "text-emerald-400 animate-pulse"
                        : ag.status === "SYNCING"
                        ? "text-violet-400"
                        : "text-cyan-400"
                    }`}
                  >
                    {ag.status}
                  </span>
                  <span className="text-zinc-500">CYCLES: {ag.cycleCount}</span>
                </div>
              </div>

              {/* Progress bar */}
              <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden mb-1">
                <div
                  className="h-full transition-all duration-300"
                  style={{
                    width: `${ag.progress}%`,
                    backgroundColor: ag.badgeColor,
                  }}
                />
              </div>

              <div className="flex items-center justify-between text-[9px] text-zinc-400">
                <span className="truncate max-w-[210px] text-zinc-400">{ag.currentTask}</span>
                <span className="text-zinc-500 flex items-center gap-0.5">
                  <Cpu className="w-2.5 h-2.5 text-zinc-400" /> {ag.cpuLoadPercent}% CPU
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
