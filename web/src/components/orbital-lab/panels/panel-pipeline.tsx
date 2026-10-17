"use client";

import React from "react";
import { ManuscriptState } from "@/data/orbital-lab/manuscript";
import { FileText, Cpu, CheckCircle2, Sigma, Layers } from "lucide-react";

interface PanelPipelineProps {
  manuscript: ManuscriptState;
  isProcessing: boolean;
}

export function PanelPipeline({ manuscript, isProcessing }: PanelPipelineProps) {
  return (
    <div className="flex flex-col h-full bg-[#070b14] border border-cyan-950/70 rounded-lg p-3 text-xs font-mono text-zinc-300 shadow-inner overflow-hidden">
      {/* Panel Header */}
      <div className="flex items-center justify-between border-b border-cyan-900/40 pb-2 mb-2">
        <div className="flex items-center gap-1.5 text-cyan-400 font-bold tracking-wider">
          <FileText className="w-3.5 h-3.5 text-cyan-400" />
          <span>[01] EXTRACTION // PIPELINE</span>
        </div>
        <div className="flex items-center gap-2">
          {isProcessing ? (
            <span className="flex items-center gap-1 text-[10px] text-amber-400 animate-pulse">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
              PARSING
            </span>
          ) : (
            <span className="flex items-center gap-1 text-[10px] text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              SYNCED
            </span>
          )}
        </div>
      </div>

      {/* Quick Stats Pill Grid */}
      <div className="grid grid-cols-4 gap-1.5 mb-2.5">
        <div className="bg-zinc-900/80 border border-zinc-800 rounded p-1.5 text-center">
          <div className="text-[10px] text-zinc-500">WORDS</div>
          <div className="text-cyan-300 font-bold">{manuscript.totalWords.toLocaleString()}</div>
        </div>
        <div className="bg-zinc-900/80 border border-zinc-800 rounded p-1.5 text-center">
          <div className="text-[10px] text-zinc-500">EQUATIONS</div>
          <div className="text-emerald-300 font-bold">{manuscript.totalEquations}</div>
        </div>
        <div className="bg-zinc-900/80 border border-zinc-800 rounded p-1.5 text-center">
          <div className="text-[10px] text-zinc-500">FIGURES</div>
          <div className="text-violet-300 font-bold">{manuscript.totalFigures}</div>
        </div>
        <div className="bg-zinc-900/80 border border-zinc-800 rounded p-1.5 text-center">
          <div className="text-[10px] text-zinc-500">SECTIONS</div>
          <div className="text-amber-300 font-bold">{manuscript.sectionsCount}</div>
        </div>
      </div>

      {/* Section Parsing Breakdown */}
      <div className="flex-1 overflow-y-auto space-y-1.5 pr-1 text-[11px] scrollbar-thin scrollbar-thumb-cyan-900/40">
        {manuscript.sections.map((sec) => (
          <div
            key={sec.id}
            className="p-1.5 rounded bg-zinc-950/60 border border-zinc-800/80 hover:border-cyan-700/50 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="text-zinc-200 font-semibold truncate max-w-[200px]">{sec.title}</span>
              <span className="text-cyan-400 font-bold">{sec.completeness}%</span>
            </div>
            {/* Progress bar */}
            <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-cyan-500 to-emerald-400 transition-all duration-500"
                style={{ width: `${sec.completeness}%` }}
              />
            </div>
            <div className="flex items-center gap-3 mt-1 text-[9px] text-zinc-500">
              <span>{sec.paragraphs} paras</span>
              {sec.equations.length > 0 && (
                <span className="text-emerald-400/90 flex items-center gap-0.5">
                  <Sigma className="w-2.5 h-2.5" /> {sec.equations.length} eqns
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
