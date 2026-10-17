"use client";

import React, { useState } from "react";
import { JournalNode } from "@/data/orbital-lab/journals";
import { Grid, Sparkles, Filter, ExternalLink } from "lucide-react";

interface PanelMatrixProps {
  journals: JournalNode[];
  selectedJournalId: string | null;
  onSelectJournal: (journal: JournalNode) => void;
}

export function PanelMatrix({ journals, selectedJournalId, onSelectJournal }: PanelMatrixProps) {
  const [filterQuartile, setFilterQuartile] = useState<string>("ALL");

  const filteredJournals = journals
    .filter((j) => (filterQuartile === "ALL" ? true : j.quartile === filterQuartile))
    .sort((a, b) => b.fitScore - a.fitScore);

  return (
    <div className="flex flex-col h-full bg-[#070b14] border border-cyan-950/70 rounded-lg p-3 text-xs font-mono text-zinc-300 shadow-inner overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-cyan-900/40 pb-2 mb-2">
        <div className="flex items-center gap-1.5 text-cyan-400 font-bold tracking-wider">
          <Grid className="w-3.5 h-3.5 text-cyan-400" />
          <span>[06] JOURNAL FIT INDEX // MATRIX</span>
        </div>
        <div className="flex items-center gap-1">
          {["ALL", "Q1", "Q2"].map((q) => (
            <button
              key={q}
              onClick={() => setFilterQuartile(q)}
              className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                filterQuartile === q
                  ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40"
                  : "text-zinc-500 hover:text-zinc-300"
              }`}
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Heat Matrix Table */}
      <div className="flex-1 overflow-y-auto space-y-1.5 pr-1 scrollbar-thin scrollbar-thumb-cyan-950 text-[11px]">
        {filteredJournals.map((j) => {
          const isSelected = selectedJournalId === j.id;
          const isHigh = j.fitScore >= 90;

          return (
            <div
              key={j.id}
              onClick={() => onSelectJournal(j)}
              className={`p-1.5 rounded cursor-pointer transition-all border ${
                isSelected
                  ? "bg-cyan-950/40 border-cyan-400 shadow-[0_0_10px_rgba(6,182,212,0.2)]"
                  : "bg-zinc-950/70 border-zinc-800/80 hover:border-cyan-800/50"
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-1.5">
                  <span className="font-bold text-zinc-100">{j.shortName}</span>
                  <span className="px-1 py-0.2 rounded text-[9px] bg-zinc-800 text-zinc-400 font-semibold">
                    {j.quartile}
                  </span>
                  <span className="text-[9px] text-zinc-500">IF {j.impactFactor}</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span
                    className={`font-bold ${
                      isHigh
                        ? "text-emerald-400"
                        : j.fitScore >= 80
                        ? "text-cyan-400"
                        : "text-amber-400"
                    }`}
                  >
                    {j.fitScore}%
                  </span>
                </div>
              </div>

              {/* Heat bar */}
              <div className="w-full h-1.5 bg-zinc-900 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{
                    width: `${j.fitScore}%`,
                    backgroundColor:
                      isHigh ? "#10b981" : j.fitScore >= 80 ? "#06b6d4" : "#f59e0b",
                  }}
                />
              </div>

              <div className="flex items-center justify-between text-[9px] text-zinc-500 mt-1">
                <span className="truncate max-w-[210px]">{j.requirements.latexTemplate}</span>
                <span className="text-zinc-400">ACC: {j.acceptanceRate}%</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
