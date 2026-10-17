import { ReactNode } from "react";

interface StepProps {
  number: number;
  title: string;
  children: ReactNode;
}

export function Step({ number, title, children }: StepProps) {
  return (
    <div className="relative flex gap-4 pb-8 last:pb-0 group">
      {/* Connector line between steps */}
      <div className="absolute left-[15px] top-8 bottom-0 w-px bg-border group-last:hidden" />
      {/* Step number badge */}
      <div className="relative z-10 flex-none w-8 h-8 rounded-full border border-brand/40 bg-background flex items-center justify-center text-brand font-mono font-bold text-sm">
        {number}
      </div>
      <div className="flex-1 min-w-0 pt-0.5">
        <h3 className="font-semibold text-foreground mt-0 mb-2">
          {title}
        </h3>
        <div className="text-muted-foreground text-sm [&>p]:mb-2">
          {children}
        </div>
      </div>
    </div>
  );
}

interface StepListProps {
  children: ReactNode;
}

export function StepList({ children }: StepListProps) {
  return <div className="mb-8">{children}</div>;
}
