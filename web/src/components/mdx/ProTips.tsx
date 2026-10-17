import { ReactNode } from "react";
import { Lightbulb } from "lucide-react";

interface TipProps {
  title: string;
  children: ReactNode;
}

export function Tip({ title, children }: TipProps) {
  return (
    <div className="rounded-lg border border-border bg-muted/50 p-4 transition-colors hover:border-brand/40">
      <div className="flex items-center gap-2 mb-2">
        <Lightbulb className="w-4 h-4 shrink-0 text-brand" />
        <h4 className="text-sm font-semibold text-foreground">
          {title}
        </h4>
      </div>
      <div className="text-sm text-muted-foreground [&>p]:mb-0">
        {children}
      </div>
    </div>
  );
}

interface ProTipsProps {
  children: ReactNode;
}

export function ProTips({ children }: ProTipsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">{children}</div>
  );
}
