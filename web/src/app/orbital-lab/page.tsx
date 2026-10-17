"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import Link from "next/link";
import { CanvasOrbital } from "@/components/orbital-lab/canvas-orbital";
import { PanelPipeline } from "@/components/orbital-lab/panels/panel-pipeline";
import { PanelSimulation } from "@/components/orbital-lab/panels/panel-simulation";
import { PanelMethod } from "@/components/orbital-lab/panels/panel-method";
import { PanelMetrics } from "@/components/orbital-lab/panels/panel-metrics";
import { PanelAgents } from "@/components/orbital-lab/panels/panel-agents";
import { PanelMatrix } from "@/components/orbital-lab/panels/panel-matrix";
import { PanelBudget } from "@/components/orbital-lab/panels/panel-budget";
import { PanelTimeline } from "@/components/orbital-lab/panels/panel-timeline";
import { JournalDetailModal } from "@/components/orbital-lab/journal-detail-modal";
import { ManuscriptEditorModal } from "@/components/orbital-lab/manuscript-editor-modal";

import { JOURNALS_DATA, JournalNode } from "@/data/orbital-lab/journals";
import { KIOTOPAPER_MANUSCRIPT, ManuscriptState } from "@/data/orbital-lab/manuscript";
import { INITIAL_SWARM_AGENTS, SwarmAgent } from "@/data/orbital-lab/agents";

import {
  Orbit,
  Play,
  Pause,
  RotateCcw,
  Volume2,
  VolumeX,
  FileEdit,
  ExternalLink,
  ChevronLeft,
  Sparkles,
  Radio,
  Sliders,
} from "lucide-react";

export default function OrbitalLabPage() {
  const [journals, setJournals] = useState<JournalNode[]>(JOURNALS_DATA);
  const [manuscript, setManuscript] = useState<ManuscriptState>(KIOTOPAPER_MANUSCRIPT);
  const [agents, setAgents] = useState<SwarmAgent[]>(INITIAL_SWARM_AGENTS);

  const [selectedJournal, setSelectedJournal] = useState<JournalNode | null>(null);
  const [inspectJournal, setInspectJournal] = useState<JournalNode | null>(null);
  const [isEditorOpen, setIsEditorOpen] = useState(false);

  const [swarmActive, setSwarmActive] = useState(true);
  const [pulseTrigger, setPulseTrigger] = useState(0);
  const [soundEnabled, setSoundEnabled] = useState(false);
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>("AG-01");

  // Audio synthesis ref
  const audioCtxRef = useRef<AudioContext | null>(null);

  const playChirp = useCallback(
    (freq = 880, duration = 0.05) => {
      if (!soundEnabled) return;
      try {
        if (!audioCtxRef.current) {
          audioCtxRef.current = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)();
        }
        const ctx = audioCtxRef.current;
        if (ctx.state === "suspended") ctx.resume();

        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(freq * 1.5, ctx.currentTime + duration);

        gain.gain.setValueAtTime(0.04, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);

        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + duration);
      } catch (err) {
        // audio context not allowed yet
      }
    },
    [soundEnabled]
  );

  // Swarm event loop
  useEffect(() => {
    if (!swarmActive) return;

    const interval = setInterval(() => {
      setPulseTrigger((p) => p + 1);

      setAgents((prevAgents) =>
        prevAgents.map((ag) => {
          const loadInc = Math.floor(Math.random() * 15) - 7;
          const newCpu = Math.max(5, Math.min(85, ag.cpuLoadPercent + loadInc));
          return {
            ...ag,
            cycleCount: ag.cycleCount + 1,
            cpuLoadPercent: newCpu,
            progress: (ag.progress + 4) % 100,
          };
        })
      );

      // Random audio telemetry tick
      if (Math.random() > 0.4) {
        playChirp(700 + Math.random() * 600, 0.035);
      }
    }, 1800);

    return () => clearInterval(interval);
  }, [swarmActive, playChirp]);

  const handleStepSwarm = () => {
    setPulseTrigger((p) => p + 1);
    setAgents((prev) =>
      prev.map((ag) => ({
        ...ag,
        cycleCount: ag.cycleCount + 1,
        progress: (ag.progress + 15) % 100,
      }))
    );
    playChirp(960, 0.08);
  };

  const handleSelectJournal = useCallback((j: JournalNode) => {
    setSelectedJournal(j);
    setInspectJournal(j);
    playChirp(1200, 0.05);
  }, [playChirp]);

  const handleManuscriptSave = (updated: ManuscriptState) => {
    setManuscript(updated);
    // Recalculate journal scores with subtle variations
    setJournals((prev) =>
      prev.map((j) => {
        const delta = Math.floor(Math.random() * 5) - 2;
        const newScore = Math.max(50, Math.min(99, j.fitScore + delta));
        return { ...j, fitScore: newScore };
      })
    );
    // Trigger swarm visual surge
    setPulseTrigger((p) => p + 5);
    playChirp(1400, 0.12);
  };

  return (
    <div className="flex flex-col w-full min-h-screen bg-[#04060c] text-zinc-100 font-mono select-none overflow-x-hidden">
      {/* Top Mission Control Header */}
      <header className="sticky top-0 z-30 flex items-center justify-between px-4 py-2.5 bg-[#070b14]/90 backdrop-blur border-b border-cyan-950/80 shadow-md">
        {/* Left: Branding & Back Navigation */}
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="flex items-center gap-1.5 px-2 py-1 rounded bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-cyan-300 hover:border-cyan-700/60 transition-colors text-xs"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
            <span>PORTAL</span>
          </Link>
          <div className="flex items-center gap-2">
            <Orbit className="w-5 h-5 text-cyan-400 animate-spin-slow" />
            <div>
              <div className="flex items-center gap-2 font-bold text-sm tracking-widest text-cyan-300">
                <span>ANTIGRAVITY // ORBITAL PAPER LAB</span>
                <span className="px-1.5 py-0.2 rounded text-[9px] bg-cyan-500/20 text-cyan-400 border border-cyan-500/40">
                  REAL-TIME SWARM
                </span>
              </div>
              <div className="text-[10px] text-zinc-500 flex items-center gap-2">
                <span>TARGET: KIOTOPAPER NOTEBOOK</span>
                <span>·</span>
                <span className="text-emerald-400">10 ORBITAL NODES ONLINE</span>
              </div>
            </div>
          </div>
        </div>

        {/* Center: Swarm Status Indicator */}
        <div className="hidden lg:flex items-center gap-4 text-xs">
          <div className="flex items-center gap-2 px-2.5 py-1 rounded bg-zinc-950 border border-cyan-900/50 text-[11px]">
            <Radio className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
            <span className="text-zinc-400">TELEMETRY:</span>
            <span className="text-cyan-300 font-bold">{swarmActive ? "AUTONOMOUS LOOP" : "PAUSED"}</span>
          </div>
          <div className="text-[11px] text-zinc-400">
            TOTAL CYCLES: <span className="text-white font-bold">{agents.reduce((acc, a) => acc + a.cycleCount, 0)}</span>
          </div>
        </div>

        {/* Right: Controls Bar */}
        <div className="flex items-center gap-2">
          {/* Audio toggle */}
          <button
            onClick={() => {
              setSoundEnabled(!soundEnabled);
              playChirp(800, 0.05);
            }}
            title={soundEnabled ? "Disable Telemetry Audio" : "Enable Telemetry Audio"}
            className={`p-1.5 rounded border text-xs transition-colors ${
              soundEnabled
                ? "bg-cyan-500/20 border-cyan-500/50 text-cyan-300"
                : "bg-zinc-900 border-zinc-800 text-zinc-500 hover:text-zinc-300"
            }`}
          >
            {soundEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
          </button>

          {/* Edit Manuscript / Kiotopaper trigger */}
          <button
            onClick={() => setIsEditorOpen(true)}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded bg-zinc-900 hover:bg-zinc-800 border border-cyan-800/60 text-cyan-300 text-xs font-bold transition-colors"
          >
            <FileEdit className="w-3.5 h-3.5" />
            <span>EDIT PAPER</span>
          </button>

          {/* Swarm Loop Toggle */}
          <button
            onClick={() => setSwarmActive(!swarmActive)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-bold transition-all ${
              swarmActive
                ? "bg-amber-500/20 text-amber-300 border border-amber-500/50 shadow-[0_0_12px_rgba(245,158,11,0.25)]"
                : "bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 hover:bg-emerald-500/30"
            }`}
          >
            {swarmActive ? (
              <>
                <Pause className="w-3.5 h-3.5" /> PAUSE SWARM
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5" /> DISPATCH SWARM
              </>
            )}
          </button>
        </div>
      </header>

      {/* Main Split Screen View */}
      <main className="flex-1 flex flex-col">
        {/* UPPER HALF: 3D WebGL Orbital Canvas */}
        <section className="relative w-full h-[45vh] min-h-[350px] shrink-0 border-b border-cyan-950/80 overflow-hidden">
          <CanvasOrbital
            journals={journals}
            selectedJournalId={selectedJournal?.id || null}
            onSelectJournal={handleSelectJournal}
            pulseTrigger={pulseTrigger}
            swarmActive={swarmActive}
          />
        </section>

        {/* LOWER HALF: Bottom Lab Grid (8 Submodules) */}
        <section className="flex-1 p-2.5 bg-[#030509]">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2.5">
            {/* Module 1: Extraction / Pipeline */}
            <div className="h-64">
              <PanelPipeline manuscript={manuscript} isProcessing={swarmActive} />
            </div>

            {/* Module 2: Particle / Simulation Solver */}
            <div className="h-64">
              <PanelSimulation swarmActive={swarmActive} />
            </div>

            {/* Module 3: Method Workspace */}
            <div className="h-64">
              <PanelMethod manuscript={manuscript} />
            </div>

            {/* Module 4: Validation / Sample Metrics */}
            <div className="h-64">
              <PanelMetrics manuscript={manuscript} swarmActive={swarmActive} />
            </div>

            {/* Module 5: Agent Dispatch & Activity */}
            <div className="h-64">
              <PanelAgents
                agents={agents}
                swarmActive={swarmActive}
                onToggleSwarm={() => setSwarmActive(!swarmActive)}
                onStepSwarm={handleStepSwarm}
                selectedAgentId={selectedAgentId}
                onSelectAgent={(id) => setSelectedAgentId(id)}
              />
            </div>

            {/* Module 6: Journal Fit Index (Matrix) */}
            <div className="h-64">
              <PanelMatrix
                journals={journals}
                selectedJournalId={selectedJournal?.id || null}
                onSelectJournal={handleSelectJournal}
              />
            </div>

            {/* Module 7: Budget & APC Tracker */}
            <div className="h-64">
              <PanelBudget journals={journals} selectedJournal={selectedJournal} />
            </div>

            {/* Module 8: Timeline & Deadlines */}
            <div className="h-64">
              <PanelTimeline
                journals={journals}
                selectedJournal={selectedJournal}
                onSelectJournal={handleSelectJournal}
              />
            </div>
          </div>
        </section>
      </main>

      {/* Journal Inspector Modal */}
      <JournalDetailModal
        journal={inspectJournal}
        onClose={() => setInspectJournal(null)}
        onSetAsPrimary={(j) => setSelectedJournal(j)}
      />

      {/* Kiotopaper Manuscript Editor Modal */}
      <ManuscriptEditorModal
        manuscript={manuscript}
        isOpen={isEditorOpen}
        onClose={() => setIsEditorOpen(false)}
        onSave={handleManuscriptSave}
      />
    </div>
  );
}
