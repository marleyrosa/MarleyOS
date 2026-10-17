"use client";

import React, { useState, useEffect } from "react";
import { JournalNode } from "@/data/orbital-lab/journals";
import { Clock, Calendar, AlertCircle, ArrowUpRight } from "lucide-react";

interface PanelTimelineProps {
  journals: JournalNode[];
  selectedJournal: JournalNode | null;
  onSelectJournal: (journal: JournalNode) => void;
}

export function PanelTimeline({ journals, selectedJournal, onSelectJournal }: PanelTimelineProps) {
  // Real-time ticking seconds
  const [secondsTick, setSecondsTick] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setSecondsTick((prev) => (prev + 1) % 60);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Sort journals by nearest deadline
  const sortedByDeadline = [...journals].sort((a, b) => a.deadlineDays - b.deadlineDays);

  const nearest = sortedByDeadline[0];

  return (
    <div className="flex flex-col h-full bg-[#070b14] border border-cyan-950/70 rounded-lg p-3 text-xs font-mono text-zinc-300 shadow-inner overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-cyan-900/40 pb-2 mb-2">
        <div className="flex items-center gap-1.5 text-cyan-400 font-bold tracking-wider">
          <Clock className="w-3.5 h-3.5 text-amber-400" />
          <span>[08] TIMELINE & DEADLINES</span>
        </div>
        <span className="text-[10px] text-amber-400 font-bold animate-pulse">
          CLOSEST: {nearest.deadlineDays}d
        </span>
      </div>

      {/* Main Countdown Display for Closest Conference */}
      <div className="p-2.5 rounded bg-zinc-950/80 border border-amber-500/30 shadow-[0_0_12px_rgba(245,158,11,0.1)] mb-2">
        <div className="flex items-center justify-between mb-1.5">
          <span className="font-bold text-amber-300 text-xs">{nearest.name}</span>
          <span className="px-1.5 py-0.2 rounded text-[9px] bg-amber-500/20 text-amber-300 font-bold">
            CALL CLOSING
          </span>
        </div>

        {/* 4 Digit Clock Grid */}
        <div className="grid grid-cols-4 gap-1.5 text-center">
          <div className="bg-zinc-900 border border-zinc-800 rounded p-1">
            <div className="text-base font-bold text-amber-400 font-mono">{nearest.deadlineDays}</div>
            <div className="text-[8px] text-zinc-500">DAYS</div>
          </div>
          <div className="bg-zinc-900 border border-zinc-800 rounded p-1">
            <div className="text-base font-bold text-amber-400 font-mono">14</div>
            <div className="text-[8px] text-zinc-500">HOURS</div>
          </div>
          <div className="bg-zinc-900 border border-zinc-800 rounded p-1">
            <div className="text-base font-bold text-amber-400 font-mono">32</div>
            <div className="text-[8px] text-zinc-500">MINS</div>
          </div>
          <div className="bg-zinc-900 border border-zinc-800 rounded p-1">
            <div className="text-base font-bold text-cyan-400 font-mono">
              {String(59 - secondsTick).padStart(2, "0")}
            </div>
            <div className="text-[8px] text-zinc-500">SECS</div>
          </div>
        </div>
      </div>

      {/* Upcoming Submission Horizons */}
      <div className="flex-1 overflow-y-auto space-y-1.5 pr-1 scrollbar-thin scrollbar-thumb-cyan-950 text-[10.5px]">
        {sortedByDeadline.slice(1, 5).map((j) => (
          <div
            key={j.id}
            onClick={() => onSelectJournal(j)}
            className="flex items-center justify-between p-1.5 rounded bg-zinc-950/60 border border-zinc-800/80 hover:border-amber-500/40 cursor-pointer transition-colors"
          >
            <div className="flex items-center gap-1.5">
              <Calendar className="w-3 h-3 text-zinc-500" />
              <span className="font-semibold text-zinc-200">{j.shortName}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-zinc-400 text-[10px]">{j.deadlineDate}</span>
              <span
                className={`font-bold ${
                  j.deadlineDays < 35 ? "text-amber-400" : "text-cyan-400"
                }`}
              >
                {j.deadlineDays}d
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
