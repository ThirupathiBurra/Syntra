import { cn } from "@/lib/utils";
import { CheckCircle2, CircleDashed, AlertCircle, Clock, Box } from "lucide-react";

export type StatusType = 
  | "running" 
  | "completed" 
  | "failed" 
  | "waiting_approval" 
  | "indexed" 
  | "processing" 
  | "error";

interface StatusBadgeProps {
  status: StatusType;
  className?: string;
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  switch (status) {
    case "running":
    case "processing":
      return (
        <div className={cn("inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium border border-indigo-500/20 bg-indigo-500/10 text-indigo-400", className)}>
          <CircleDashed className="h-3.5 w-3.5 animate-spin" />
          <span className="capitalize">{status.replace("_", " ")}</span>
        </div>
      );
    case "completed":
    case "indexed":
      return (
        <div className={cn("inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium border border-emerald-500/20 bg-emerald-500/10 text-emerald-400", className)}>
          <CheckCircle2 className="h-3.5 w-3.5" />
          <span className="capitalize">{status.replace("_", " ")}</span>
        </div>
      );
    case "failed":
    case "error":
      return (
        <div className={cn("inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium border border-red-500/20 bg-red-500/10 text-red-400", className)}>
          <AlertCircle className="h-3.5 w-3.5" />
          <span className="capitalize">{status.replace("_", " ")}</span>
        </div>
      );
    case "waiting_approval":
      return (
        <div className={cn("inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium border border-amber-500/20 bg-amber-500/10 text-amber-400", className)}>
          <Clock className="h-3.5 w-3.5" />
          <span className="capitalize">Waiting Approval</span>
        </div>
      );
    default:
      return (
        <div className={cn("inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium border border-zinc-500/20 bg-zinc-500/10 text-zinc-400", className)}>
          <Box className="h-3.5 w-3.5" />
          <span className="capitalize">{String(status)}</span>
        </div>
      );
  }
}
