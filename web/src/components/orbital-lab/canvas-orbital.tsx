"use client";

import React, { useEffect, useRef, useState, useCallback } from "react";
import * as THREE from "three";
import { JournalNode } from "@/data/orbital-lab/journals";
import { Eye, RotateCcw, ZoomIn, ZoomOut, Compass, Sparkles } from "lucide-react";

interface CanvasOrbitalProps {
  journals: JournalNode[];
  selectedJournalId: string | null;
  onSelectJournal: (journal: JournalNode) => void;
  pulseTrigger: number;
  swarmActive: boolean;
}

export function CanvasOrbital({
  journals,
  selectedJournalId,
  onSelectJournal,
  pulseTrigger,
  swarmActive,
}: CanvasOrbitalProps) {
  const mountRef = useRef<HTMLDivElement>(null);
  const [hoveredJournal, setHoveredJournal] = useState<JournalNode | null>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  // Default to 2D Radar on mobile for 100% instant rendering guarantee, or user can toggle 3D WebGL
  const [mode, setMode] = useState<"2d" | "3d">("2d");

  // Keep latest references for callbacks and props so effects NEVER re-run unnecessarily
  const onSelectJournalRef = useRef(onSelectJournal);
  const journalsRef = useRef(journals);
  const swarmActiveRef = useRef(swarmActive);
  const pulseTriggerRef = useRef(pulseTrigger);

  onSelectJournalRef.current = onSelectJournal;
  journalsRef.current = journals;
  swarmActiveRef.current = swarmActive;
  pulseTriggerRef.current = pulseTrigger;

  // Camera and zoom refs
  const rotRef = useRef({ x: 0.45, y: -0.25, targetX: 0.45, targetY: -0.25, distance: 22 });
  const scale2DRef = useRef(1.0);
  const angleOffset2DRef = useRef(0);

  const handleZoomIn = () => {
    rotRef.current.distance = Math.max(12, rotRef.current.distance - 3);
    scale2DRef.current = Math.min(1.6, scale2DRef.current + 0.15);
  };

  const handleZoomOut = () => {
    rotRef.current.distance = Math.min(45, rotRef.current.distance + 3);
    scale2DRef.current = Math.max(0.6, scale2DRef.current - 0.15);
  };

  const handleReset = () => {
    rotRef.current.targetX = 0.45;
    rotRef.current.targetY = -0.25;
    rotRef.current.distance = 22;
    scale2DRef.current = 1.0;
    angleOffset2DRef.current = 0;
  };

  // -------------------------------------------------------------
  // 3D WebGL Implementation (Runs ONLY when mode === "3d")
  // -------------------------------------------------------------
  useEffect(() => {
    if (mode !== "3d") return;

    const container = mountRef.current;
    if (!container) return;

    const getSafeDims = () => {
      const rect = container.getBoundingClientRect();
      const w = rect.width || container.clientWidth || window.innerWidth || 360;
      const h = rect.height || container.clientHeight || 360;
      return {
        w: Math.max(200, Math.floor(w)),
        h: Math.max(200, Math.floor(h)),
      };
    };

    let { w, h } = getSafeDims();
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let renderer: THREE.WebGLRenderer;
    let reqId: number;

    try {
      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(54, w / h, 0.1, 1000);
      camera.position.set(0, 12, rotRef.current.distance);
      camera.lookAt(0, 0, 0);

      renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: false,
        powerPreference: "default",
      });

      renderer.setSize(w, h);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      renderer.setClearColor(0x04060c, 1);

      renderer.domElement.style.position = "absolute";
      renderer.domElement.style.top = "0";
      renderer.domElement.style.left = "0";
      renderer.domElement.style.width = "100%";
      renderer.domElement.style.height = "100%";
      renderer.domElement.style.display = "block";
      renderer.domElement.style.touchAction = "none";

      container.innerHTML = "";
      container.appendChild(renderer.domElement);

      renderer.domElement.addEventListener("webglcontextlost", (e) => {
        e.preventDefault();
        console.warn("WebGL context lost! Switching to 2D Radar mode.");
        setMode("2d");
      });
    } catch (err) {
      console.warn("WebGL init failed, switching to 2D:", err);
      setMode("2d");
      return;
    }

    // 1. Starfield
    const starGeo = new THREE.BufferGeometry();
    const starCount = 350;
    const starPos = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount; i++) {
      const r = 25 + Math.random() * 50;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      starPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      starPos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      starPos[i * 3 + 2] = r * Math.cos(phi);
    }
    starGeo.setAttribute("position", new THREE.BufferAttribute(starPos, 3));
    const starMat = new THREE.PointsMaterial({ size: 1.5, color: 0x38bdf8 });
    scene.add(new THREE.Points(starGeo, starMat));

    // 2. Core Pulsar
    const coreGroup = new THREE.Group();
    scene.add(coreGroup);

    const coreMesh = new THREE.Mesh(
      new THREE.IcosahedronGeometry(2.4, 2),
      new THREE.MeshBasicMaterial({ color: 0x06b6d4, wireframe: true })
    );
    coreGroup.add(coreMesh);

    const nucleusMesh = new THREE.Mesh(
      new THREE.SphereGeometry(1.5, 20, 20),
      new THREE.MeshBasicMaterial({ color: 0x38bdf8 })
    );
    coreGroup.add(nucleusMesh);

    const centerMesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.7, 16, 16),
      new THREE.MeshBasicMaterial({ color: 0xffffff })
    );
    coreGroup.add(centerMesh);

    // 3. Volumetric 3D Torus Rings
    const ringRadii = [6.0, 10.5, 15.0];
    const ringColors = [0x06b6d4, 0x0ea5e9, 0x38bdf8];

    ringRadii.forEach((radius, idx) => {
      const torusMesh = new THREE.Mesh(
        new THREE.TorusGeometry(radius, 0.08, 8, 80),
        new THREE.MeshBasicMaterial({ color: ringColors[idx], transparent: true, opacity: 0.7 })
      );
      torusMesh.rotation.x = Math.PI / 2;
      scene.add(torusMesh);
    });

    // 4. Nodes
    const nodesMap = new Map<string, THREE.Mesh>();
    const photonList: Array<{ mesh: THREE.Mesh; progress: number; speed: number; target: THREE.Vector3 }> = [];

    journalsRef.current.forEach((j) => {
      const r = ringRadii[j.orbitRing - 1] || ringRadii[1];
      const x = Math.cos(j.orbitAngle) * r;
      const z = Math.sin(j.orbitAngle) * r;
      const y = Math.sin(j.orbitAngle * 3) * 0.6;

      const isOpt = j.fitScore >= 90;
      const color = isOpt ? 0x10b981 : j.status === "Critical Window" ? 0xf59e0b : 0x06b6d4;

      const nodeMesh = new THREE.Mesh(
        new THREE.OctahedronGeometry(isOpt ? 1.1 : 0.8, 0),
        new THREE.MeshBasicMaterial({ color })
      );
      nodeMesh.position.set(x, y, z);
      nodeMesh.userData = { journal: j };
      scene.add(nodeMesh);
      nodesMap.set(j.id, nodeMesh);

      // Halo
      const halo = new THREE.Mesh(
        new THREE.TorusGeometry(isOpt ? 1.5 : 1.2, 0.04, 6, 20),
        new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.8 })
      );
      halo.rotation.x = Math.PI / 2;
      nodeMesh.add(halo);

      // Beam
      const beamGeo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(x, y, z),
      ]);
      const beam = new THREE.Line(
        beamGeo,
        new THREE.LineBasicMaterial({ color, transparent: true, opacity: isOpt ? 0.5 : 0.25 })
      );
      scene.add(beam);

      // Photon
      const photon = new THREE.Mesh(
        new THREE.SphereGeometry(0.22, 6, 6),
        new THREE.MeshBasicMaterial({ color: 0xffffff })
      );
      scene.add(photon);
      photonList.push({
        mesh: photon,
        progress: Math.random(),
        speed: 0.005 + Math.random() * 0.005,
        target: new THREE.Vector3(x, y, z),
      });
    });

    const updateSize = () => {
      const dims = getSafeDims();
      camera.aspect = dims.w / dims.h;
      camera.updateProjectionMatrix();
      renderer.setSize(dims.w, dims.h, false);
      renderer.render(scene, camera);
    };

    let ro: ResizeObserver | null = null;
    if (typeof ResizeObserver !== "undefined") {
      ro = new ResizeObserver(() => updateSize());
      ro.observe(container);
    }
    window.addEventListener("resize", updateSize);
    updateSize();

    // 5. Animation loop
    const startTime = performance.now();
    const animate = () => {
      reqId = requestAnimationFrame(animate);
      try {
        const time = (performance.now() - startTime) * 0.001;
        const rot = rotRef.current;

        rot.x += (rot.targetX - rot.x) * 0.06;
        rot.y += (rot.targetY - rot.y) * 0.06;

        const camDist = rot.distance;
        camera.position.x = camDist * Math.sin(rot.y) * Math.cos(rot.x);
        camera.position.y = camDist * Math.sin(rot.x);
        camera.position.z = camDist * Math.cos(rot.y) * Math.cos(rot.x);
        camera.lookAt(0, 0, 0);

        const pulse = 1.0 + Math.sin(time * 3.5) * 0.08;
        coreGroup.scale.set(pulse, pulse, pulse);
        coreMesh.rotation.y = time * 0.4;
        nucleusMesh.rotation.y = -time * 0.25;

        journalsRef.current.forEach((j) => {
          const mesh = nodesMap.get(j.id);
          if (mesh) {
            const currentAngle = j.orbitAngle + time * j.orbitSpeed * (swarmActiveRef.current ? 1.6 : 1.0);
            const r = ringRadii[j.orbitRing - 1] || ringRadii[1];
            mesh.position.x = Math.cos(currentAngle) * r;
            mesh.position.z = Math.sin(currentAngle) * r;
            mesh.position.y = Math.sin(currentAngle * 2.5) * 0.6;
            mesh.rotation.y += 0.02;
          }
        });

        photonList.forEach((p, idx) => {
          const j = journalsRef.current[idx];
          const mesh = nodesMap.get(j?.id);
          if (mesh) {
            p.target.copy(mesh.position);
            p.progress += p.speed * (swarmActiveRef.current ? 1.8 : 1.0);
            if (p.progress > 1.0) p.progress = 0;
            p.mesh.position.lerpVectors(new THREE.Vector3(0, 0, 0), p.target, p.progress);
          }
        });

        renderer.render(scene, camera);
      } catch (err) {
        console.error("Three.js loop error:", err);
      }
    };
    animate();

    // Interaction
    const isDraggingRef = { current: false };
    const dragStart = { x: 0, y: 0 };

    const onPointerDown = (clientX: number, clientY: number) => {
      isDraggingRef.current = true;
      dragStart.x = clientX;
      dragStart.y = clientY;

      // Raycasting
      const rect = container.getBoundingClientRect();
      const raycaster = new THREE.Raycaster();
      const p = new THREE.Vector2(
        ((clientX - rect.left) / rect.width) * 2 - 1,
        -((clientY - rect.top) / rect.height) * 2 + 1
      );
      raycaster.setFromCamera(p, camera);
      const hits = raycaster.intersectObjects(Array.from(nodesMap.values()), false);
      if (hits.length > 0) {
        const hit = hits[0].object as THREE.Mesh;
        if (hit.userData.journal) {
          onSelectJournalRef.current(hit.userData.journal as JournalNode);
        }
      }
    };

    const onPointerMove = (clientX: number, clientY: number) => {
      if (!isDraggingRef.current) return;
      const dx = clientX - dragStart.x;
      const dy = clientY - dragStart.y;
      dragStart.x = clientX;
      dragStart.y = clientY;

      if (Number.isFinite(dx) && Number.isFinite(dy)) {
        rotRef.current.targetY -= dx * 0.008;
        rotRef.current.targetX = Math.max(0.08, Math.min(Math.PI / 2.2, rotRef.current.targetX - dy * 0.007));
      }
    };

    const onMouseDown = (e: MouseEvent) => onPointerDown(e.clientX, e.clientY);
    const onMouseMove = (e: MouseEvent) => onPointerMove(e.clientX, e.clientY);
    const onMouseUp = () => { isDraggingRef.current = false; };

    const onTouchStart = (e: TouchEvent) => {
      if (e.touches.length === 1) onPointerDown(e.touches[0].clientX, e.touches[0].clientY);
    };
    const onTouchMove = (e: TouchEvent) => {
      if (e.touches.length === 1) onPointerMove(e.touches[0].clientX, e.touches[0].clientY);
    };
    const onTouchEnd = () => { isDraggingRef.current = false; };

    container.addEventListener("mousedown", onMouseDown);
    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);

    container.addEventListener("touchstart", onTouchStart, { passive: true });
    window.addEventListener("touchmove", onTouchMove, { passive: true });
    window.addEventListener("touchend", onTouchEnd);

    return () => {
      cancelAnimationFrame(reqId);
      if (ro) ro.disconnect();
      window.removeEventListener("resize", updateSize);

      container.removeEventListener("mousedown", onMouseDown);
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);

      container.removeEventListener("touchstart", onTouchStart);
      window.removeEventListener("touchmove", onTouchMove);
      window.removeEventListener("touchend", onTouchEnd);

      if (renderer && renderer.domElement && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      if (renderer) renderer.dispose();
    };
  }, [mode]);

  return (
    <div className="relative w-full h-full min-h-[350px] overflow-hidden select-none bg-[#04060c]">
      {/* 2D High-Performance Radar (Active by default for 100% mobile guarantee) */}
      {mode === "2d" && (
        <Canvas2DFallback
          journalsRef={journalsRef}
          onSelectJournalRef={onSelectJournalRef}
          swarmActiveRef={swarmActiveRef}
          scaleRef={scale2DRef}
          angleOffsetRef={angleOffset2DRef}
        />
      )}

      {/* 3D WebGL Canvas Container */}
      {mode === "3d" && (
        <div
          ref={mountRef}
          className="absolute inset-0 w-full h-full cursor-grab active:cursor-grabbing touch-none"
        />
      )}

      {/* Top Left HUD Telemetry Header */}
      <div className="absolute top-3 left-3 z-20 pointer-events-none flex flex-col gap-1 font-mono text-xs text-cyan-400/90 max-w-[65%]">
        <div className="flex items-center gap-2">
          <span className="inline-block w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_8px_#06b6d4]" />
          <span className="font-bold tracking-widest text-xs sm:text-sm text-cyan-200 truncate">
            {mode === "2d" ? "RADAR ORBITAL [2D]" : "SIMULADOR 3D [WEBGL]"}
          </span>
        </div>
        <div className="text-[10px] text-zinc-400">
          NÚCLEO: <span className="text-cyan-300">KIOTOPAPER</span> · 10 ÓRBITAS ATIVAS
        </div>
      </div>

      {/* Top Right Mobile Controls HUD */}
      <div className="absolute top-3 right-3 z-20 flex items-center gap-1.5 font-mono text-[11px]">
        {/* Mode Toggle Button */}
        <button
          onClick={() => setMode((m) => (m === "2d" ? "3d" : "2d"))}
          className={`px-2.5 py-1 rounded border font-bold flex items-center gap-1 transition-all ${
            mode === "3d"
              ? "bg-amber-500/25 text-amber-300 border-amber-500/60 shadow-[0_0_10px_rgba(245,158,11,0.3)]"
              : "bg-cyan-500/25 text-cyan-300 border-cyan-500/60 shadow-[0_0_10px_rgba(6,182,212,0.3)]"
          }`}
          title="Alternar entre Radar 2D e 3D WebGL"
        >
          <Compass className="w-3.5 h-3.5" />
          <span>{mode === "2d" ? "ATIVAR 3D" : "ATIVAR 2D"}</span>
        </button>

        {/* Zoom In */}
        <button
          onClick={handleZoomIn}
          className="p-1.5 rounded bg-zinc-900/90 border border-zinc-700 hover:border-cyan-500 text-zinc-300 hover:text-white transition-colors"
          title="Zoom In"
        >
          <ZoomIn className="w-3.5 h-3.5" />
        </button>

        {/* Zoom Out */}
        <button
          onClick={handleZoomOut}
          className="p-1.5 rounded bg-zinc-900/90 border border-zinc-700 hover:border-cyan-500 text-zinc-300 hover:text-white transition-colors"
          title="Zoom Out"
        >
          <ZoomOut className="w-3.5 h-3.5" />
        </button>

        {/* Reset Camera */}
        <button
          onClick={handleReset}
          className="p-1.5 rounded bg-zinc-900/90 border border-zinc-700 hover:border-cyan-500 text-zinc-300 hover:text-white transition-colors"
          title="Resetar Câmera"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Floating 3D Hover Tooltip HUD */}
      {hoveredJournal && (
        <div
          className="absolute z-30 pointer-events-none transform -translate-x-1/2 -translate-y-full mb-3 px-3 py-2 rounded-lg border border-cyan-500/40 bg-zinc-950/95 backdrop-blur-md shadow-[0_0_20px_rgba(6,182,212,0.35)] text-xs font-mono text-zinc-200 min-w-[200px] max-w-[280px]"
          style={{
            left: `${Math.max(110, Math.min(window.innerWidth - 110, mousePos.x))}px`,
            top: `${Math.max(90, mousePos.y)}px`,
          }}
        >
          <div className="flex items-center justify-between gap-2 border-b border-cyan-900/60 pb-1 mb-1">
            <span className="font-bold text-cyan-300 text-xs sm:text-sm">{hoveredJournal.shortName}</span>
            <span className="px-1 py-0.2 rounded text-[9px] font-bold bg-emerald-500/20 text-emerald-300">
              {hoveredJournal.fitScore}%
            </span>
          </div>
          <div className="text-[10px] text-zinc-400 grid grid-cols-2 gap-1">
            <span>{hoveredJournal.quartile} (IF {hoveredJournal.impactFactor})</span>
            <span className="text-amber-400 font-semibold">{hoveredJournal.deadlineDays}d restantes</span>
          </div>
          <div className="mt-1 text-[9px] text-cyan-400">TOQUE PARA ABRIR REQUISITOS →</div>
        </div>
      )}
    </div>
  );
}

// -------------------------------------------------------------
// 2D High-Fidelity Radar Component (100% Reliable & Touch-Interactive)
// -------------------------------------------------------------
function Canvas2DFallback({
  journalsRef,
  onSelectJournalRef,
  swarmActiveRef,
  scaleRef,
  angleOffsetRef,
}: {
  journalsRef: React.MutableRefObject<JournalNode[]>;
  onSelectJournalRef: React.MutableRefObject<(j: JournalNode) => void>;
  swarmActiveRef: React.MutableRefObject<boolean>;
  scaleRef: React.MutableRefObject<number>;
  angleOffsetRef: React.MutableRefObject<number>;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;
    let t = 0;

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const w = rect.width || window.innerWidth || 360;
      const h = rect.height || 360;

      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      ctx.scale(dpr, dpr);
    };
    resize();
    window.addEventListener("resize", resize);

    const render = () => {
      animId = requestAnimationFrame(render);
      t += swarmActiveRef.current ? 0.016 : 0.009;

      const rect = canvas.getBoundingClientRect();
      const w = rect.width || canvas.width;
      const h = rect.height || canvas.height;
      const cx = w / 2;
      const cy = h / 2;

      // Dark background
      ctx.fillStyle = "#04060c";
      ctx.fillRect(0, 0, w, h);

      // Starfield dots
      ctx.fillStyle = "rgba(34, 211, 238, 0.45)";
      for (let i = 0; i < 60; i++) {
        const sx = ((i * 137.5) % w);
        const sy = ((i * 293.7) % h);
        ctx.fillRect(sx, sy, 1.5, 1.5);
      }

      // Orbital Concentric Rings
      const baseMaxR = Math.min(cx, cy) * 0.84 * scaleRef.current;
      const rings = [baseMaxR * 0.36, baseMaxR * 0.65, baseMaxR * 0.95];

      rings.forEach((r, idx) => {
        // Glowing ring
        ctx.strokeStyle = idx === 0 ? "rgba(6, 182, 212, 0.5)" : idx === 1 ? "rgba(14, 165, 233, 0.35)" : "rgba(56, 189, 248, 0.25)";
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.stroke();

        // Dashed radar pattern
        ctx.setLineDash([4, 8]);
        ctx.strokeStyle = "rgba(6, 182, 212, 0.18)";
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);
      });

      // Central Pulsar Core (Kiotopaper Manuscript)
      const pulse = 18 + Math.sin(t * 4) * 3;
      const coreGrad = ctx.createRadialGradient(cx, cy, 2, cx, cy, pulse * 1.8);
      coreGrad.addColorStop(0, "#ffffff");
      coreGrad.addColorStop(0.3, "#38bdf8");
      coreGrad.addColorStop(0.7, "rgba(6, 182, 212, 0.4)");
      coreGrad.addColorStop(1, "rgba(6, 182, 212, 0)");

      ctx.fillStyle = coreGrad;
      ctx.beginPath();
      ctx.arc(cx, cy, pulse * 1.8, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#06b6d4";
      ctx.beginPath();
      ctx.arc(cx, cy, pulse * 0.75, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(cx, cy, 4.5, 0, Math.PI * 2);
      ctx.fill();

      // Journal Nodes
      const currentJournals = journalsRef.current;
      currentJournals.forEach((j) => {
        const ringIdx = j.orbitRing - 1;
        const r = rings[ringIdx] || rings[1];
        const angle = j.orbitAngle + t * j.orbitSpeed * 2.2 + angleOffsetRef.current;
        const nx = cx + Math.cos(angle) * r;
        const ny = cy + Math.sin(angle) * r;

        // Beam from Core
        ctx.strokeStyle = j.fitScore >= 90 ? "rgba(16, 185, 129, 0.35)" : "rgba(6, 182, 212, 0.22)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(nx, ny);
        ctx.stroke();

        // Traveling Photon Packet
        const photonProg = ((t * 0.85 + j.orbitRing * 0.32) % 1);
        const px = cx + (nx - cx) * photonProg;
        const py = cy + (ny - cy) * photonProg;
        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(px, py, 2.5, 0, Math.PI * 2);
        ctx.fill();

        // Node Glow
        const isOpt = j.fitScore >= 90;
        ctx.fillStyle = isOpt ? "#10b981" : j.status === "Critical Window" ? "#f59e0b" : "#06b6d4";
        ctx.beginPath();
        ctx.arc(nx, ny, 7.5, 0, Math.PI * 2);
        ctx.fill();

        // Node Halo Ring
        ctx.strokeStyle = isOpt ? "#34d399" : "#38bdf8";
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.arc(nx, ny, 11, 0, Math.PI * 2);
        ctx.stroke();

        // Node Label
        ctx.font = "bold 10px monospace";
        ctx.fillStyle = "#ffffff";
        ctx.shadowColor = "#000000";
        ctx.shadowBlur = 4;
        ctx.fillText(j.shortName, nx + 13, ny + 4);
        ctx.shadowBlur = 0;
      });
    };

    render();

    // Touch Drag / Tap handlers
    let isDragging = false;
    let startX = 0;

    const handlePointerDown = (clientX: number, clientY: number) => {
      isDragging = true;
      startX = clientX;

      const rect = canvas.getBoundingClientRect();
      const clickX = clientX - rect.left;
      const clickY = clientY - rect.top;
      const cx = (rect.width || canvas.width) / 2;
      const cy = (rect.height || canvas.height) / 2;
      const baseMaxR = Math.min(cx, cy) * 0.84 * scaleRef.current;
      const rings = [baseMaxR * 0.36, baseMaxR * 0.65, baseMaxR * 0.95];

      // Proximity hit test
      journalsRef.current.forEach((j) => {
        const ringIdx = j.orbitRing - 1;
        const r = rings[ringIdx] || rings[1];
        const angle = j.orbitAngle + t * j.orbitSpeed * 2.2 + angleOffsetRef.current;
        const nx = cx + Math.cos(angle) * r;
        const ny = cy + Math.sin(angle) * r;
        if (Math.hypot(clickX - nx, clickY - ny) < 28) {
          onSelectJournalRef.current(j);
        }
      });
    };

    const handlePointerMove = (clientX: number) => {
      if (!isDragging) return;
      const dx = clientX - startX;
      startX = clientX;
      if (Number.isFinite(dx)) {
        angleOffsetRef.current += dx * 0.008;
      }
    };

    const onMouseDown = (e: MouseEvent) => handlePointerDown(e.clientX, e.clientY);
    const onMouseMove = (e: MouseEvent) => handlePointerMove(e.clientX);
    const onMouseUp = () => { isDragging = false; };

    const onTouchStart = (e: TouchEvent) => {
      if (e.touches.length === 1) handlePointerDown(e.touches[0].clientX, e.touches[0].clientY);
    };
    const onTouchMove = (e: TouchEvent) => {
      if (e.touches.length === 1) handlePointerMove(e.touches[0].clientX);
    };
    const onTouchEnd = () => { isDragging = false; };

    canvas.addEventListener("mousedown", onMouseDown);
    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);

    canvas.addEventListener("touchstart", onTouchStart, { passive: true });
    window.addEventListener("touchmove", onTouchMove, { passive: true });
    window.addEventListener("touchend", onTouchEnd);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", resize);

      canvas.removeEventListener("mousedown", onMouseDown);
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);

      canvas.removeEventListener("touchstart", onTouchStart);
      window.removeEventListener("touchmove", onTouchMove);
      window.removeEventListener("touchend", onTouchEnd);
    };
  }, []); // Run ONCE on mount, NEVER torn down

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full block touch-none cursor-grab active:cursor-grabbing"
    />
  );
}
