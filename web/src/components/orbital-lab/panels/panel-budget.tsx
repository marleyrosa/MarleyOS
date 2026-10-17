"use client";

import React, { useState } from "react";
import { JournalNode } from "@/data/orbital-lab/journals";
import { DollarSign, Coins, ShieldCheck, ArrowRightLeft } from "lucide-react";

interface PanelBudgetProps {
  journals: JournalNode[];
  selectedJournal: JournalNode | null;
}

export function PanelBudget({ journals, selectedJournal }: PanelBudgetProps) {
  const [currency, setCurrency] = useState<"usd" | "eur" | "brl">("brl");
  const [fundingOffset, setFundingOffset] = useState<number>(50); // 50% institutional grant

  const formatPrice = (costObj: { usd: number; eur: number; brl: number }) => {
    if (currency === "usd") return `$${costObj.usd.toLocaleString()}`;
    if (currency === "eur") return `€${costObj.eur.toLocaleString()}`;
    return `R$ ${costObj.brl.toLocaleString()}`;
  };

  const activeJournal = selectedJournal || journals[0];
  const fullPrice = activeJournal.apcCost[currency];
  const payablePrice = fullPrice * (1 - fundingOffset / 100);

  return (
    <div className="flex flex-col h-full bg-[#070b14] border border-cyan-950/70 rounded-lg p-3 text-xs font-mono text-zinc-300 shadow-inner overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-cyan-900/40 pb-2 mb-2">
        <div className="flex items-center gap-1.5 text-cyan-400 font-bold tracking-wider">
          <Coins className="w-3.5 h-3.5 text-amber-400" />
          <span>[07] BUDGET & APC TRACKER</span>
        </div>
        <div className="flex items-center gap-1">
          {(["usd", "eur", "brl"] as const).map((curr) => (
            <button
              key={curr}
              onClick={() => setCurrency(curr)}
              className={`px-1.5 py-0.5 rounded text-[10px] uppercase font-bold ${
                currency === curr
                  ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                  : "text-zinc-500 hover:text-zinc-300"
              }`}
            >
              {curr}
            </button>
          ))}
        </div>
      </div>

      {/* Target Journal Snapshot */}
      <div className="p-2 rounded bg-zinc-950/70 border border-zinc-800/80 mb-2">
        <div className="flex items-center justify-between mb-1">
          <span className="font-bold text-zinc-200">{activeJournal.shortName}</span>
          <span className="text-[10px] text-zinc-400">{activeJournal.openAccessType}</span>
        </div>
        <div className="flex items-baseline justify-between mt-1">
          <span className="text-[11px] text-zinc-400">ESTIMATED APC:</span>
          <span className="text-base font-bold text-amber-400 font-mono">
            {formatPrice(activeJournal.apcCost)}
          </span>
        </div>
        {fundingOffset > 0 && (
          <div className="flex items-baseline justify-between text-[10px] text-emerald-400 border-t border-zinc-900 pt-1 mt-1">
            <span>AFTER GRANT (-{fundingOffset}%):</span>
            <span className="font-bold">
              {currency === "usd" ? `$${payablePrice.toFixed(0)}` : currency === "eur" ? `€${payablePrice.toFixed(0)}` : `R$ ${payablePrice.toFixed(0)}`}
            </span>
          </div>
        )}
      </div>

      {/* Institutional Funding Slider */}
      <div className="mb-2">
        <div className="flex justify-between text-[10px] text-zinc-400 mb-1">
          <span>INSTITUTIONAL / CNPq OFFSET</span>
          <span className="text-cyan-300 font-bold">{fundingOffset}%</span>
        </div>
        <input
          type="range"
          min="0"
          max="100"
          step="5"
          value={fundingOffset}
          onChange={(e) => setFundingOffset(Number(e.target.value))}
          className="w-full h-1 bg-zinc-800 rounded appearance-none cursor-pointer accent-amber-400"
        />
      </div>

      {/* Quick comparison of top 3 */}
      <div className="flex-1 overflow-y-auto space-y-1 text-[10px]">
        {journals.slice(0, 3).map((j) => (
          <div
            key={j.id}
            className="flex items-center justify-between p-1 rounded bg-zinc-900/40 border border-zinc-800/40 text-zinc-400"
          >
            <span className="truncate max-w-[140px] text-zinc-300">{j.shortName}</span>
            <span className="font-mono text-amber-300 font-semibold">{formatPrice(j.apcCost)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
