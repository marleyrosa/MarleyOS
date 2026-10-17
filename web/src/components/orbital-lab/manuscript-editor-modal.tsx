"use client";

import React, { useState } from "react";
import { ManuscriptState } from "@/data/orbital-lab/manuscript";
import { X, Save, Sparkles, BookOpen, Layers, Check } from "lucide-react";

interface ManuscriptEditorModalProps {
  manuscript: ManuscriptState;
  isOpen: boolean;
  onClose: () => void;
  onSave: (updated: ManuscriptState) => void;
}

export function ManuscriptEditorModal({
  manuscript,
  isOpen,
  onClose,
  onSave,
}: ManuscriptEditorModalProps) {
  const [title, setTitle] = useState(manuscript.title);
  const [abstract, setAbstract] = useState(manuscript.abstract);
  const [totalWords, setTotalWords] = useState(manuscript.totalWords);
  const [rmse, setRmse] = useState(manuscript.hilBenchmarks.rmseErrorPercent);

  if (!isOpen) return null;

  const handleSave = () => {
    const updated: ManuscriptState = {
      ...manuscript,
      title,
      abstract,
      totalWords,
      hilBenchmarks: {
        ...manuscript.hilBenchmarks,
        rmseErrorPercent: rmse,
      },
    };
    onSave(updated);
    onClose();
  };

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

        {/* Header */}
        <div className="flex items-center gap-2 border-b border-cyan-900/60 pb-3 mb-4 pr-8">
          <BookOpen className="w-4 h-4 text-cyan-400" />
          <div>
            <h2 className="text-base font-bold text-white tracking-wide">
              KIOTOPAPER // MANUSCRIPT AST EDITOR
            </h2>
            <p className="text-[10px] text-zinc-400">
              Modifications immediately trigger swarm real-time recalculation (AG-01..AG-05)
            </p>
          </div>
        </div>

        {/* Form Body */}
        <div className="space-y-3 mb-4">
          <div>
            <label className="block text-[10px] text-zinc-400 uppercase font-bold mb-1">
              Manuscript Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-2.5 py-1.5 rounded bg-zinc-950 border border-zinc-800 text-zinc-100 font-mono focus:border-cyan-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-[10px] text-zinc-400 uppercase font-bold mb-1">
              Abstract & Scope Summary
            </label>
            <textarea
              rows={4}
              value={abstract}
              onChange={(e) => setAbstract(e.target.value)}
              className="w-full px-2.5 py-1.5 rounded bg-zinc-950 border border-zinc-800 text-zinc-100 font-mono text-[11px] leading-relaxed focus:border-cyan-500 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-[10px] text-zinc-400 uppercase font-bold mb-1">
                Total Words: {totalWords}
              </label>
              <input
                type="number"
                value={totalWords}
                onChange={(e) => setTotalWords(Number(e.target.value))}
                className="w-full px-2.5 py-1.5 rounded bg-zinc-950 border border-zinc-800 text-cyan-300 font-mono focus:border-cyan-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-[10px] text-zinc-400 uppercase font-bold mb-1">
                HIL Emulation RMSE Error (%): {rmse}
              </label>
              <input
                type="number"
                step="0.005"
                value={rmse}
                onChange={(e) => setRmse(Number(e.target.value))}
                className="w-full px-2.5 py-1.5 rounded bg-zinc-950 border border-zinc-800 text-emerald-300 font-mono focus:border-cyan-500 focus:outline-none"
              />
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between border-t border-zinc-800 pt-3">
          <span className="text-[10px] text-zinc-500">
            Kiotopaper Notebook ID: 187aaeb3-485f-47f9-8421-aff2417b517e
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-3 py-1.5 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-700 transition-colors"
            >
              CANCEL
            </button>
            <button
              onClick={handleSave}
              className="flex items-center gap-1.5 px-4 py-1.5 rounded bg-cyan-600 hover:bg-cyan-500 text-white font-bold transition-all shadow-[0_0_15px_rgba(6,182,212,0.3)]"
            >
              <Save className="w-3.5 h-3.5" /> RE-CALCULATE SWARM
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
