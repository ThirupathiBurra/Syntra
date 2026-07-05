"use client";

import { Bell, Search, MonitorPlay, MonitorOff, ChevronDown, Wand2 } from "lucide-react";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter } from "next/navigation";

export function Topbar() {
  const router = useRouter();
  const [isPresentationMode, setIsPresentationMode] = useState(false);
  const [showDemoMenu, setShowDemoMenu] = useState(false);

  useEffect(() => {
    if (isPresentationMode) {
      document.documentElement.classList.add("presentation-mode");
    } else {
      document.documentElement.classList.remove("presentation-mode");
    }
  }, [isPresentationMode]);

  const togglePresentationMode = () => {
    setIsPresentationMode(!isPresentationMode);
  };

  const executeDemo = (scenario: string) => {
    setShowDemoMenu(false);
    router.push(`/workflows/preview?q=${encodeURIComponent(scenario)}`);
  };

  return (
    <header className="sticky top-0 z-40 flex h-14 w-full items-center justify-between border-b border-zinc-800/50 bg-zinc-950/80 backdrop-blur-xl px-4 sm:px-6 lg:px-8">
      <div className="flex flex-1 items-center gap-x-4">
        <div className="flex w-full max-w-sm items-center gap-x-3 rounded-full bg-zinc-900 px-3 py-1.5 border border-zinc-800/50">
          <Search className="h-4 w-4 text-zinc-500" />
          <input
            type="text"
            className="flex-1 bg-transparent text-sm text-zinc-300 placeholder:text-zinc-500 focus:outline-none"
            placeholder="Search missions, knowledge..."
          />
          <div className="flex items-center gap-1 rounded bg-zinc-800 px-1.5 py-0.5 text-xs text-zinc-400">
            <span>⌘</span>
            <span>K</span>
          </div>
        </div>
      </div>
      <div className="flex items-center gap-x-4">
        
        {/* Demo Scenarios Dropdown */}
        <div className="relative">
          <button 
            onClick={() => setShowDemoMenu(!showDemoMenu)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-medium text-amber-500 bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/20 transition-colors"
          >
            <Wand2 className="h-3 w-3" />
            Demo Scenarios
            <ChevronDown className="h-3 w-3 opacity-50" />
          </button>
          
          <AnimatePresence>
            {showDemoMenu && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="absolute right-0 mt-2 w-56 rounded-xl border border-zinc-800 bg-zinc-950 shadow-2xl py-1 z-50"
              >
                <div className="px-3 py-2 border-b border-zinc-800/50 mb-1">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-500">Quick Execute</span>
                </div>
                <button onClick={() => executeDemo("Employee Onboarding")} className="w-full text-left px-4 py-2 text-sm text-zinc-300 hover:bg-zinc-900 hover:text-white transition-colors">Employee Onboarding</button>
                <button onClick={() => executeDemo("Contract Review")} className="w-full text-left px-4 py-2 text-sm text-zinc-300 hover:bg-zinc-900 hover:text-white transition-colors">Contract Review</button>
                <button onClick={() => executeDemo("Customer Complaint")} className="w-full text-left px-4 py-2 text-sm text-zinc-300 hover:bg-zinc-900 hover:text-white transition-colors">Customer Complaint</button>
                <button onClick={() => executeDemo("Compliance Audit")} className="w-full text-left px-4 py-2 text-sm text-zinc-300 hover:bg-zinc-900 hover:text-white transition-colors">Compliance Audit</button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Presentation Mode Toggle */}
        <button 
          onClick={togglePresentationMode} 
          className={`flex items-center justify-center h-8 w-8 rounded-md transition-all ${isPresentationMode ? 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30' : 'text-zinc-400 hover:text-zinc-100 hover:bg-zinc-900'}`}
          title={isPresentationMode ? "Disable Presentation Mode" : "Enable Presentation Mode"}
        >
          {isPresentationMode ? <MonitorOff className="h-4 w-4" /> : <MonitorPlay className="h-4 w-4" />}
        </button>

        <div className="h-4 w-px bg-zinc-800"></div>

        <button type="button" className="text-zinc-400 hover:text-zinc-100 transition-colors">
          <span className="sr-only">View notifications</span>
          <Bell className="h-5 w-5" aria-hidden="true" />
        </button>
      </div>
    </header>
  );
}
