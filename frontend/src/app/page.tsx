"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Search, Sparkles, Building2, Briefcase, FileText, Code2, MoveRight, Activity, ShieldCheck, Layers, Cpu, Mic } from "lucide-react";
import { motion } from "framer-motion";


function AnimatedCounter({ value, duration = 2 }: { value: number, duration?: number }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = value;
    const incrementTime = (duration * 1000) / end;
    
    const timer = setInterval(() => {
      start += 1;
      setCount(start);
      if (start >= end) clearInterval(timer);
    }, incrementTime);

    return () => clearInterval(timer);
  }, [value, duration]);

  return <span>{count}</span>;
}

export default function MissionControl() {
  const router = useRouter();
  const [command, setCommand] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showKPIs, setShowKPIs] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setShowKPIs(true), 400);
    return () => clearTimeout(timer);
  }, []);

  const templates = [
    {
      title: "Financial Audit",
      industry: "Finance",
      icon: Building2,
      description: "Analyze Q3 reports against new compliance policies and flag discrepancies.",
      color: "text-amber-500",
      bg: "bg-amber-500/10",
      border: "border-amber-500/20"
    },
    {
      title: "Legal Contract Review",
      industry: "Legal",
      icon: Briefcase,
      description: "Review vendor agreements for liability clauses and extract key terms.",
      color: "text-indigo-500",
      bg: "bg-indigo-500/10",
      border: "border-indigo-500/20"
    },
    {
      title: "Market Analysis",
      industry: "Strategy",
      icon: FileText,
      description: "Compile competitor pricing models from Q1 and generate a strategy brief.",
      color: "text-emerald-500",
      bg: "bg-emerald-500/10",
      border: "border-emerald-500/20"
    },
    {
      title: "Codebase Refactoring",
      industry: "Engineering",
      icon: Code2,
      description: "Analyze legacy monolithic services and propose microservices architecture.",
      color: "text-cyan-500",
      bg: "bg-cyan-500/10",
      border: "border-cyan-500/20"
    }
  ];

  const [isListening, setIsListening] = useState(false);

  const handleVoiceCommand = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert("Speech recognition is not supported in this browser. Please use Chrome.");
      return;
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const SpeechRecognition = (window as any).webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.continuous = false;
    recognition.interimResults = true;
    
    recognition.onstart = () => {
      setIsListening(true);
    };
    
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    recognition.onresult = (event: any) => {
      let interimTranscript = '';
      let finalTranscript = '';
      
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        } else {
          interimTranscript += event.results[i][0].transcript;
        }
      }
      
      setCommand(finalTranscript || interimTranscript);
    };
    
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    recognition.onerror = (event: any) => {
      console.error(event.error);
      setIsListening(false);
    };
    
    recognition.onend = () => {
      setIsListening(false);
    };
    
    if (isListening) {
      // We can't easily stop it without keeping the instance, 
      // but it naturally stops when they stop speaking.
      setIsListening(false);
    } else {
      recognition.start();
    }
  };

  const handleCommandSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!command.trim() || isLoading) return;
    
    setIsLoading(true);
    try {
      // In Milestone 15, we navigate to the preview/intercept page for generative workflows.
      router.push(`/workflows/preview?q=${encodeURIComponent(command)}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-full flex-col items-center justify-start max-w-5xl mx-auto pt-8 pb-24 px-4 md:pt-16">
      
      {/* Executive KPI Dashboard */}
      <div className="w-full grid grid-cols-2 md:grid-cols-4 gap-4 mb-16 h-24">
        {showKPIs && (
          <>
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-4 flex flex-col justify-center shadow-xl group hover:border-indigo-500/30 transition-colors">
              <div className="flex items-center gap-2 mb-1">
                <Activity className="h-4 w-4 text-indigo-400" />
                <span className="text-xs text-zinc-500 uppercase tracking-wider">Active Missions</span>
              </div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-zinc-200"><AnimatedCounter value={24} duration={1} /></div>
            </motion.div>
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-4 flex flex-col justify-center shadow-xl group hover:border-amber-500/30 transition-colors">
              <div className="flex items-center gap-2 mb-1">
                <ShieldCheck className="h-4 w-4 text-amber-400" />
                <span className="text-xs text-zinc-500 uppercase tracking-wider">Pending Approvals</span>
              </div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-zinc-200"><AnimatedCounter value={8} duration={1.5} /></div>
            </motion.div>
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-4 flex flex-col justify-center shadow-xl group hover:border-emerald-500/30 transition-colors">
              <div className="flex items-center gap-2 mb-1">
                <Layers className="h-4 w-4 text-emerald-400" />
                <span className="text-xs text-zinc-500 uppercase tracking-wider">Indexed Documents</span>
              </div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-zinc-200"><AnimatedCounter value={142} duration={2} /></div>
            </motion.div>
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-4 flex flex-col justify-center shadow-xl group hover:border-cyan-500/30 transition-colors">
              <div className="flex items-center gap-2 mb-1">
                <Cpu className="h-4 w-4 text-cyan-400" />
                <span className="text-xs text-zinc-500 uppercase tracking-wider">AI Success Rate</span>
              </div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-zinc-200"><AnimatedCounter value={99} duration={2} />%</div>
            </motion.div>
          </>
        )}
      </div>

      {/* Hero Section */}
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-12"
      >
        <div className="inline-flex items-center rounded-full border border-indigo-500/30 bg-indigo-500/10 px-4 py-1.5 text-sm font-medium text-indigo-300 mb-6 shadow-lg shadow-indigo-500/20">
          <Sparkles className="mr-2 h-4 w-4 animate-pulse" />
          Enterprise OS Online
        </div>
        <h1 className="text-5xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-6xl mb-6">
          What is our mission today?
        </h1>
        <p className="text-xl text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
          Command your AI workforce. Let&apos;s execute complex workflows with precision.
        </p>
      </motion.div>

      {/* Omni Command Bar */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="w-full max-w-4xl mb-16"
      >
        <form onSubmit={handleCommandSubmit} className="relative group">
          <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-indigo-500/30 via-zinc-300 dark:via-zinc-800 to-indigo-500/30 opacity-50 blur transition duration-500 group-hover:opacity-100"></div>
          <div className="relative flex items-center w-full rounded-2xl bg-white/80 dark:bg-zinc-950/80 backdrop-blur-xl border border-zinc-200 dark:border-zinc-700 p-2 shadow-2xl overflow-hidden">
            <Search className="ml-4 h-6 w-6 text-indigo-500 dark:text-indigo-400" />
            <input
              type="text"
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              placeholder="E.g., Audit our Q3 financial reports against the new compliance policy..."
              className="flex-1 bg-transparent px-4 py-4 text-xl text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 dark:placeholder:text-zinc-600 focus:outline-none transition-all"
            />
            <button
              type="button"
              onClick={handleVoiceCommand}
              className={`mr-2 p-3 rounded-xl transition-all flex items-center justify-center ${
                isListening 
                  ? 'bg-rose-500/20 text-rose-500 hover:bg-rose-500/30 shadow-[0_0_15px_rgba(244,63,94,0.5)] animate-pulse' 
                  : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 hover:bg-zinc-200 dark:hover:bg-zinc-700 hover:text-zinc-800 dark:hover:text-zinc-300'
              }`}
              title="Voice Command"
            >
              {isListening ? <Mic className="h-6 w-6" /> : <Mic className="h-6 w-6" />}
            </button>
            <button 
              type="submit"
              className="mr-2 rounded-xl bg-indigo-600 px-6 py-3 font-medium text-white shadow-lg transition-all hover:bg-indigo-500 hover:shadow-indigo-500/25 active:scale-95 flex items-center text-lg"
            >
              {isLoading ? (
                <div className="h-6 w-6 border-2 border-white/20 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  Execute
                  <MoveRight className="ml-2 h-5 w-5" />
                </>
              )}
            </button>
          </div>
        </form>
      </motion.div>

      {/* Mission Templates */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="w-full max-w-4xl"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-sm font-medium tracking-widest text-zinc-500 uppercase flex items-center gap-2">
            Suggested Scenarios
            <span className="bg-zinc-200 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 text-[10px] px-2 py-0.5 rounded-full">Demo Mode</span>
          </h2>
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {templates.map((template, idx) => (
            <motion.div 
              key={idx}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => {
                setCommand(template.description);
                // Auto-submit for demo flow smoothness
                const syntheticEvent = { preventDefault: () => {} } as React.FormEvent;
                setTimeout(() => handleCommandSubmit(syntheticEvent), 100);
              }}
              className="group relative flex cursor-pointer flex-col gap-3 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 p-5 transition-all hover:border-zinc-300 dark:hover:border-zinc-700 shadow-lg hover:shadow-xl"
            >
              <div className="flex items-center gap-3">
                <div className={`rounded-lg p-2 ${template.bg} ${template.border} border transition-colors group-hover:bg-opacity-20`}>
                  <template.icon className={`h-5 w-5 ${template.color}`} />
                </div>
                <div className="text-sm font-semibold text-zinc-900 dark:text-zinc-200">{template.title}</div>
              </div>
              <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed group-hover:text-zinc-800 dark:group-hover:text-zinc-300 transition-colors">
                {template.description}
              </p>
              <div className="absolute top-5 right-5 text-xs font-semibold text-zinc-500 dark:text-zinc-600 group-hover:text-indigo-500 dark:group-hover:text-indigo-400 transition-colors">
                {template.industry}
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
