import { motion } from "framer-motion";
import { ReactNode } from "react";

interface PageHeaderProps {
  title: string;
  description?: string;
  icon?: React.ElementType;
  action?: ReactNode;
}

export function PageHeader({ title, description, icon: Icon, action }: PageHeaderProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8"
    >
      <div className="flex items-center gap-3">
        {Icon && (
          <div className="p-2 rounded-xl bg-zinc-900 border border-zinc-800 text-zinc-400">
            <Icon className="h-6 w-6" />
          </div>
        )}
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-zinc-100">{title}</h1>
          {description && (
            <p className="text-sm text-zinc-400 mt-1">{description}</p>
          )}
        </div>
      </div>
      {action && (
        <div className="flex items-center gap-2">
          {action}
        </div>
      )}
    </motion.div>
  );
}
