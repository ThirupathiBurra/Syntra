import { motion } from "framer-motion";
import { ReactNode } from "react";
import { Search } from "lucide-react";

interface EmptyStateProps {
  title: string;
  description: string;
  icon?: React.ElementType;
  action?: ReactNode;
}

export function EmptyState({ title, description, icon: Icon = Search, action }: EmptyStateProps) {
  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col items-center justify-center py-16 text-center border border-dashed border-zinc-800 rounded-2xl bg-zinc-900/20"
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-zinc-900 border border-zinc-800 mb-4">
        <Icon className="h-6 w-6 text-zinc-500" />
      </div>
      <h3 className="text-sm font-medium text-zinc-200">{title}</h3>
      <p className="mt-1 text-sm text-zinc-500 max-w-sm">{description}</p>
      {action && (
        <div className="mt-6">
          {action}
        </div>
      )}
    </motion.div>
  );
}
