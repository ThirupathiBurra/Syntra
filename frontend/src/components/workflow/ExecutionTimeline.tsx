"use client";

import { CheckCircle2, Clock, PlayCircle, FileText } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";

export function ExecutionTimeline() {
  const [baseTime] = useState(new Date());

  const events = [
    {
      id: 1,
      type: "completed",
      title: "Workflow Initialized",
      description: "Mission: Execute requested business logic",
      time: new Date(baseTime.getTime() + 0).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' }),
      icon: PlayCircle,
      color: "text-indigo-500",
      bg: "bg-indigo-500/10",
      border: "border-indigo-500/20"
    },
    {
      id: 2,
      type: "completed",
      title: "Plan Generated",
      description: "Conductor built a multi-step execution graph",
      time: new Date(baseTime.getTime() + 5000).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' }),
      icon: CheckCircle2,
      color: "text-emerald-500",
      bg: "bg-emerald-500/10",
      border: "border-emerald-500/20"
    },
    {
      id: 3,
      type: "completed",
      title: "Enterprise Knowledge Retrieved",
      description: "Found relevant policy chunks from Knowledge Base",
      time: new Date(baseTime.getTime() + 15000).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' }),
      icon: FileText,
      color: "text-cyan-500",
      bg: "bg-cyan-500/10",
      border: "border-cyan-500/20",
      metric: "98% Confidence"
    },
    {
      id: 4,
      type: "in-progress",
      title: "Agent Active",
      description: "Cross-referencing parameters against compliance policy",
      time: new Date(baseTime.getTime() + 18000).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' }),
      icon: Clock,
      color: "text-amber-500",
      bg: "bg-amber-500/10",
      border: "border-amber-500/20",
      pulsing: true
    }
  ];

  return (
    <div className="space-y-4">
      {events.map((event, index) => (
        <motion.div 
          key={event.id}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3, delay: index * 0.1 }}
          className="relative flex gap-4"
        >
          {/* Timeline connecting line */}
          {index !== events.length - 1 && (
            <div className="absolute left-5 top-10 bottom-[-16px] w-px bg-zinc-800" />
          )}
          
          <div className="flex-none">
            <div className={`flex h-10 w-10 items-center justify-center rounded-full border ${event.bg} ${event.border}`}>
              {event.pulsing ? (
                <div className="relative flex h-5 w-5">
                  <span className={`absolute inline-flex h-full w-full animate-ping rounded-full opacity-75 ${event.bg.replace('/10', '')}`} />
                  <span className="relative inline-flex h-5 w-5 rounded-full items-center justify-center">
                    <event.icon className={`h-5 w-5 ${event.color}`} />
                  </span>
                </div>
              ) : (
                <event.icon className={`h-5 w-5 ${event.color}`} />
              )}
            </div>
          </div>
          
          <div className="flex-1 rounded-xl border border-zinc-800/50 bg-zinc-900/30 p-4 transition-colors hover:bg-zinc-900/50">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium text-zinc-100">{event.title}</h3>
              <span className="text-xs font-medium text-zinc-500">{event.time}</span>
            </div>
            <p className="mt-1 text-sm text-zinc-400">{event.description}</p>
            {event.metric && (
              <div className="mt-2 inline-flex items-center rounded-md border border-cyan-500/20 bg-cyan-500/10 px-2 py-1 text-xs font-medium text-cyan-400">
                {event.metric}
              </div>
            )}
          </div>
        </motion.div>
      ))}
    </div>
  );
}
