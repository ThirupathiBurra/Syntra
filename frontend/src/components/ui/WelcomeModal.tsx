"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Command, ShieldCheck, Zap, X, MoveRight, Compass } from "lucide-react";

export function WelcomeModal() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // Only show on first run for demo purposes
    const hasSeenWelcome = localStorage.getItem("syntra_welcome_seen");
    if (!hasSeenWelcome) {
      // Small delay for dramatic effect
      const timer = setTimeout(() => setIsOpen(true), 1000);
      return () => clearTimeout(timer);
    }
  }, []);

  const dismiss = () => {
    setIsOpen(false);
    localStorage.setItem("syntra_welcome_seen", "true");
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
        <motion.div 
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 10 }}
          transition={{ type: "spring", damping: 25, stiffness: 300 }}
          className="bg-zinc-950 border border-zinc-800 rounded-3xl p-8 max-w-2xl w-full shadow-2xl relative overflow-hidden"
        >
          {/* Decorative background glow */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[200px] bg-indigo-500/20 rounded-full blur-[80px] -z-10" />

          <button 
            onClick={dismiss}
            className="absolute top-6 right-6 p-2 text-zinc-500 hover:text-white rounded-full hover:bg-zinc-800 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>

          <div className="flex items-center gap-3 mb-6">
            <div className="h-12 w-12 rounded-xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center">
              <Compass className="h-6 w-6 text-indigo-400" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white tracking-tight">Welcome to Syntra</h2>
              <p className="text-indigo-400 text-sm font-medium">Enterprise AI Operating System</p>
            </div>
          </div>

          <p className="text-zinc-300 mb-8 leading-relaxed text-lg">
            Syntra is not a chatbot. It is an intelligent orchestration layer that dynamically builds and executes workflows using your enterprise knowledge.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
              <Zap className="h-5 w-5 text-amber-400 mb-3" />
              <h3 className="font-semibold text-zinc-200 mb-1">Dynamic Orchestration</h3>
              <p className="text-sm text-zinc-400">Describe a goal, and Syntra will compose the necessary capabilities into an execution graph.</p>
            </div>
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
              <ShieldCheck className="h-5 w-5 text-emerald-400 mb-3" />
              <h3 className="font-semibold text-zinc-200 mb-1">Enterprise Guardrails</h3>
              <p className="text-sm text-zinc-400">Human-in-the-loop approvals and explicit capability routing ensure secure execution.</p>
            </div>
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
              <Sparkles className="h-5 w-5 text-cyan-400 mb-3" />
              <h3 className="font-semibold text-zinc-200 mb-1">Demo Scenarios</h3>
              <p className="text-sm text-zinc-400">Use the &quot;Demo Scenarios&quot; dropdown in the Topbar for instant, high-fidelity mock executions.</p>
            </div>
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
              <Command className="h-5 w-5 text-indigo-400 mb-3" />
              <h3 className="font-semibold text-zinc-200 mb-1">Presentation Mode</h3>
              <p className="text-sm text-zinc-400">Toggle presentation mode in the top right to optimize the UI for screen sharing.</p>
            </div>
          </div>

          <div className="flex items-center justify-between mt-8 pt-6 border-t border-zinc-800">
            <div className="flex items-center gap-2 text-xs font-mono text-zinc-500">
              <span className="bg-zinc-800 px-1.5 py-0.5 rounded text-zinc-400">ESC</span> to dismiss
            </div>
            <button 
              onClick={dismiss}
              className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-xl font-medium flex items-center transition-all shadow-lg shadow-indigo-500/20 active:scale-95"
            >
              Enter Mission Control
              <MoveRight className="ml-2 h-4 w-4" />
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
