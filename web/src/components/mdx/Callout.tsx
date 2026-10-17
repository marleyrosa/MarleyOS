import { ReactNode } from "react";
import { Info, AlertTriangle, AlertCircle, Lightbulb } from "lucide-react";
import { cn } from "@/lib/utils";

type CalloutType = "info" | "warning" | "error" | "tip";

interface CalloutProps {
  type?: CalloutType;
  title?: string;
  children: ReactNode;
}

const calloutStyles: Record<
  CalloutType,
  { wrap: string; icon: typeof Info; iconColor: string }
> = {
  info: {
    wrap: "border-info/30 bg-info/5",
    icon: Info,
    iconColor: "text-info",
  },
  warning: {
    wrap: "border-warning/30 bg-warning/5",
    icon: AlertTriangle,
    iconColor: "text-warning",
  },
  error: {
    wrap: "border-destructive/30 bg-destructive/5",
    icon: AlertCircle,
    iconColor: "text-destructive",
  },
  tip: {
    wrap: "border-brand/30 bg-brand/5",
    icon: Lightbulb,
    iconColor: "text-brand",
  },
};

export function Callout({ type = "info", title, children }: CalloutProps) {
  const styles = calloutStyles[type];
  const Icon = styles.icon;

  return (
    <div
      className={cn(
        "border-l-2 border rounded-r-lg rounded-l-sm p-4 mb-4",
        styles.wrap
      )}
    >
      <div className="flex items-start gap-3">
        <Icon className={cn("w-5 h-5 mt-0.5 shrink-0", styles.iconColor)} />
        <div className="flex-1 min-w-0">
          {title && (
            <h4 className="text-sm font-semibold text-foreground mb-1">
              {title}
            </h4>
          )}
          <div className="text-sm text-muted-foreground [&>p]:mb-0">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
