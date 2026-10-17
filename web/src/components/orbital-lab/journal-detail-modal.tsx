"use client";

import React from "react";
import { JournalNode } from "@/data/orbital-lab/journals";
import { X, CheckCircle, AlertTriangle, FileCode, Clock, DollarSign, Award, ExternalLink } from "lucide-react";

interface JournalDetailModalProps {
  journal: JournalNode | null;
  onClose: () => void;
  onSetAsPrimary: (journal: JournalNode) => void;
}

export function JournalDetailModal({ journal, onClose, onSetAsPrimary }: JournalDetailModalProps) {
  if (!journal) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl bg-[#070b14] border border-cyan-500/50 rounded-xl p-5 shadow-[0_0_30px_rgba(6,182,212,0.25)] text-zinc-200 font-mono text-xs">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1 rounded-md bg-zinc-900 border border-zinc-700 hover:bg-zinc-800 text-zinc-400 hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Modal Header */}
        <div className="flex items-start justify-between border-b border-cyan-900/60 pb-3 mb-4 pr-8">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">
                {journal.publisher}
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                {journal.quartile} · IF {journal.impactFactor}
              </span>
              <span className="text-zinc-500 text-[10px]">ORBIT RING #{journal.orbitRing}</span>
            </div>
            <h2 className="text-base font-bold text-white tracking-wide">{journal.name}</h2>
            <p className="text-[11px] text-zinc-400 mt-0.5">Short Identifier: {journal.shortName}</p>
          </div>
        </div>

        {/* Scope and Fit Bar */}
        <div className="mb-4 bg-zinc-950/80 border border-zinc-800 p-3 rounded-lg">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[11px] font-bold text-cyan-400">EDITORIAL SCOPE & ADHERENCE</span>
            <span className="text-sm font-bold text-emerald-400">{journal.fitScore}% FIT SCORE</span>
          </div>
          <p className="text-zinc-300 text-[11px] leading-relaxed mb-2">{journal.scope}</p>
          <div className="w-full h-2 bg-zinc-900 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-cyan-500 to-emerald-400"
              style={{ width: `${journal.fitScore}%` }}
            />
          </div>
        </div>

        {/* Requirements Grid */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="bg-zinc-950/80 border border-zinc-800 p-3 rounded-lg space-y-2">
            <div className="text-[10px] text-zinc-400 uppercase tracking-wider font-bold">
              Submissions Requirements
            </div>
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">HIL Bench Required:</span>
              <span className={journal.requirements.hilValidationRequired ? "text-emerald-400 font-bold" : "text-zinc-400"}>
                {journal.requirements.hilValidationRequired ? "YES (MANDATORY)" : "OPTIONAL"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">LaTeX Template:</span>
              <span className="text-cyan-300 font-mono text-[10px]">{journal.requirements.latexTemplate}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">Double Blind Review:</span>
              <span className="text-zinc-200">{journal.requirements.blindReview ? "YES" : "SINGLE BLIND"}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">Code Open Access:</span>
              <span className="text-zinc-200">{journal.requirements.codeAvailability ? "RECOMMENDED" : "N/A"}</span>
            </div>
          </div>

          <div className="bg-zinc-950/80 border border-zinc-800 p-3 rounded-lg space-y-2">
            <div className="text-[10px] text-zinc-400 uppercase tracking-wider font-bold">
              Budget & Deadline Telemetry
            </div>
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">Page Limit:</span>
              <span className="text-zinc-200">{journal.pageLimit}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">APC (USD / BRL):</span>
              <span className="text-amber-400 font-bold">
                ${journal.apcCost.usd.toLocaleString()} / R$ {journal.apcCost.brl.toLocaleString()}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">OA Publishing Model:</span>
              <span className="text-cyan-300">{journal.openAccessType}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">Days to Deadline:</span>
              <span className="text-red-400 font-bold">{journal.deadlineDays} Days</span>
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between border-t border-zinc-800 pt-3">
          <span className="text-[10px] text-zinc-500">
            LAST SYNCED BY AG-03 (EDITORIAL SCOPE MATCHER)
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-3 py-1.5 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-700 transition-colors"
            >
              CLOSE
            </button>
            <button
              onClick={() => {
                onSetAsPrimary(journal);
                onClose();
              }}
              className="px-4 py-1.5 rounded bg-gradient-to-r from-cyan-600 to-emerald-600 hover:from-cyan-500 hover:to-emerald-500 text-white font-bold tracking-wider shadow-[0_0_15px_rgba(6,182,212,0.3)] transition-all"
            >
              SET AS PRIMARY TARGET
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
