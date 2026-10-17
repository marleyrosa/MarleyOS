import { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface TerminalProps {
  title?: string;
  children: ReactNode;
}

export function Terminal({ title = "agent-session", children }: TerminalProps) {
  return (
    <div className="rounded-lg border border-code-border bg-code mb-6 overflow-hidden shadow-lg">
      {/* Window chrome */}
      <div className="flex items-center gap-2 px-4 py-2.5 border-b border-code-border bg-code-title">
        <div className="flex gap-1.5">
          <span className="w-3 h-3 rounded-full bg-red-500/90" />
          <span className="w-3 h-3 rounded-full bg-amber-500/90" />
          <span className="w-3 h-3 rounded-full bg-emerald-500/90" />
        </div>
        <span className="ml-2 font-mono text-xs text-muted-foreground">{title}</span>
      </div>
      {/* Body */}
      <div className="p-4 font-mono text-sm text-code-foreground overflow-x-auto">
        {children}
      </div>
    </div>
  );
}

interface TerminalLineProps {
  type?: "user" | "agent" | "system";
  children: ReactNode;
}

export function TerminalLine({ type = "system", children }: TerminalLineProps) {
  const config = {
    user: { prompt: "$", color: "text-brand" },
    agent: { prompt: "▸", color: "text-brand" },
    system: { prompt: "", color: "text-muted-foreground" },
  };
  const { prompt, color } = config[type];

  return (
    <span className="mb-2 flex gap-2">
      {prompt && <span className={cn("font-bold shrink-0", color)}>{prompt}</span>}
      <span className="flex-1">{children}</span>
    </span>
  );
}

interface TerminalBlockProps {
  highlight?: boolean;
  children: ReactNode;
}

export function TerminalBlock({ highlight, children }: TerminalBlockProps) {
  return (
    <div
      className={cn(
        "pl-4 border-l-2 mb-4",
        highlight ? "border-brand" : "border-code-border"
      )}
    >
      {children}
    </div>
  );
}
