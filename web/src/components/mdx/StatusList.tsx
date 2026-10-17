import { ReactNode } from "react";
import { cn } from "@/lib/utils";

type Status = "running" | "done" | "pending";

interface StatusItemProps {
  status?: Status;
  label?: string;
  children: ReactNode;
}

const statusDot: Record<Status, string> = {
  running: "bg-brand animate-pulse",
  done: "bg-brand",
  pending: "bg-muted-foreground",
};

export function StatusItem({ status = "running", label, children }: StatusItemProps) {
  return (
    <span className="flex items-center gap-2">
      <span className={cn("w-2 h-2 rounded-full shrink-0", statusDot[status])} />
      <span className="text-sm">
        {label && <strong className="font-semibold">{label}:</strong>} {children}
      </span>
    </span>
  );
}

interface StatusListProps {
  children: ReactNode;
}

export function StatusList({ children }: StatusListProps) {
  return <div className="space-y-2 pl-1 mb-4">{children}</div>;
}
