"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { PlayCircle, ShieldAlert, Clock, Coins, BrainCircuit, Info, Save, X, Edit2, Loader2, CheckCircle2 } from "lucide-react";
import { useState, useEffect, Suspense } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter, useSearchParams } from "next/navigation";

import { useQuery } from "@tanstack/react-query";

interface GeneratedNode {
  node_id: string;
  capability_id: string;
  description: string;
  reasoning: string;
}

interface GeneratedWorkflow {
  workflow_id: string;
  name: string;
  description: string;
  department: string;
  tags: string[];
  confidence: number;
  estimated_duration: string;
  estimated_cost: string;
  requires_human_approval: boolean;
  nodes: GeneratedNode[];
}

const generateWorkflow = async (request: string): Promise<GeneratedWorkflow> => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/workflows/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: "user_1", request, metadata: {} }),
  });
  if (!res.ok) throw new Error("Failed to generate workflow");
  return res.json();
};

function WorkflowPreviewContent() {
  const searchParams = useSearchParams();
  const query = searchParams.get('q') || "New Workflow";
  const router = useRouter();
  
  const [isEditing, setIsEditing] = useState(false);
  const [workflowName, setWorkflowName] = useState("");
  const [progressState, setProgressState] = useState(0);
  const [isSaving, setIsSaving] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  
  const { data: workflow, isLoading, error } = useQuery({
    queryKey: ["generate", query],
    queryFn: () => generateWorkflow(query),
    staleTime: Infinity,
  });

  useEffect(() => {
    if (workflow && !workflowName) {
      setWorkflowName(workflow.name);
    }
  }, [workflow, workflowName]);
  useEffect(() => {
    const timer1 = setTimeout(() => setProgressState(1), 800); // 1 node generated
    const timer2 = setTimeout(() => setProgressState(2), 1600); // 2 nodes generated
    const timer3 = setTimeout(() => setProgressState(3), 2400); // all nodes generated
    const timer4 = setTimeout(() => setProgressState(4), 3000); // readiness analysis complete
    
    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
      clearTimeout(timer4);
    };
  }, []);

  const handleExecute = async () => {
    if (!workflow) return;
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/workflows/${workflow.workflow_id}/execute`, {
        method: "POST"
      });
      if (res.ok) {
        // Redirect to the DAG execution demo page (assuming it renders running workflows)
        router.push(`/workflows/demo`);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleSaveTemplate = async () => {
    setIsSaving(true);
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 800));
    setIsSaving(false);
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 3000); // Reset after 3s
  };

  const isReady = !!workflow && !isLoading;

  return (
    <div className="max-w-7xl mx-auto py-6 flex flex-col h-full">
      <PageHeader 
        title={isReady ? "Workflow Ready" : error ? "Generation Failed" : "Designing Workflow..."}
        description={isReady ? "Review the generated execution graph before orchestrating." : `Interpreting request: "${query}"`}
        icon={BrainCircuit}
        action={
          <div className="flex items-center gap-2">
            <button onClick={() => router.back()} className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium text-zinc-300 hover:text-white bg-zinc-800 hover:bg-zinc-700 transition-colors">
              <X className="h-4 w-4" /> Cancel
            </button>
            {isReady && (
              <>
                <button 
                  onClick={handleSaveTemplate}
                  disabled={isSaving || isSaved}
                  className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isSaved 
                      ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30" 
                      : "text-zinc-300 hover:text-white border border-zinc-700 hover:bg-zinc-800"
                  }`}
                >
                  {isSaving ? (
                    <><Loader2 className="h-4 w-4 animate-spin" /> Saving...</>
                  ) : isSaved ? (
                    <><CheckCircle2 className="h-4 w-4" /> Saved!</>
                  ) : (
                    <><Save className="h-4 w-4" /> Save Template</>
                  )}
                </button>
                <button onClick={handleExecute} className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2 rounded-lg text-sm font-medium transition-all shadow-lg shadow-indigo-500/20">
                  <PlayCircle className="h-4 w-4" /> Approve & Run
                </button>
              </>
            )}
          </div>
        }
      />

      <div className="flex-1 flex flex-col lg:flex-row gap-6">
        
        {/* Left Column: Details & Explainability */}
        <div className="w-full lg:w-1/3 space-y-6">
          <AnimatePresence>
            {progressState > 0 && (
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-zinc-950 border border-zinc-800 rounded-2xl p-6 shadow-xl relative group"
              >
                {isReady && (
                  <div className="absolute top-4 right-4">
                    <button onClick={() => setIsEditing(!isEditing)} className="p-2 text-zinc-500 hover:text-indigo-400 rounded-lg hover:bg-zinc-900 transition-colors">
                      <Edit2 className="h-4 w-4" />
                    </button>
                  </div>
                )}
                
                {isEditing ? (
                  <input 
                    type="text" 
                    value={workflowName}
                    onChange={(e) => setWorkflowName(e.target.value)}
                    className="w-full bg-zinc-900 border border-indigo-500/50 rounded-lg px-3 py-1.5 text-lg font-semibold text-zinc-100 focus:outline-none mb-2"
                  />
                ) : (
                  <h2 className="text-xl font-semibold text-zinc-100 pr-8">{workflowName}</h2>
                )}
                
                <p className="text-sm text-zinc-400 mt-2">{workflow?.description}</p>
                
                <div className="flex flex-wrap gap-2 mt-4">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded-full">{workflow?.department}</span>
                  {workflow?.tags.map(tag => (
                    <span key={tag} className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 bg-zinc-800 px-2 py-0.5 rounded-full">{tag}</span>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence>
            {progressState > 0 && (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-zinc-950 border border-zinc-800 rounded-2xl p-6 shadow-xl"
              >
                <h3 className="text-sm font-medium text-zinc-300 mb-4 flex items-center gap-2">
                  <Info className="h-4 w-4 text-indigo-400" /> Explainability
                  {!isReady && <Loader2 className="h-3 w-3 text-zinc-500 animate-spin ml-auto" />}
                </h3>
                <div className="space-y-4 relative">
                  <div className="absolute left-1 top-2 bottom-2 w-0.5 bg-zinc-800/50 rounded-full" />
                  
                  {workflow?.nodes.map((node, idx) => (
                    <motion.div 
                      key={node.node_id}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.1 }}
                      className="pl-6 relative"
                    >
                      <div className="absolute left-[1px] top-1.5 h-2 w-2 rounded-full bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.6)]" />
                      <h4 className="text-sm font-medium text-zinc-200">{node.capability_id}</h4>
                      <p className="text-xs text-zinc-500 mt-1 leading-relaxed">{node.reasoning}</p>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Right Column: Execution Readiness */}
        <div className="flex-1 flex flex-col gap-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 h-28">
            <AnimatePresence>
              {isReady && workflow && (
                <>
                  <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 }} className="bg-zinc-950 border border-zinc-800 rounded-2xl p-4 shadow-xl flex flex-col items-center justify-center text-center">
                    <BrainCircuit className="h-5 w-5 text-indigo-400 mb-2" />
                    <p className="text-xs text-zinc-500 mb-1">Confidence</p>
                    <p className="text-lg font-semibold text-zinc-200">{Math.round(workflow.confidence * 100)}%</p>
                  </motion.div>
                  <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.2 }} className="bg-zinc-950 border border-zinc-800 rounded-2xl p-4 shadow-xl flex flex-col items-center justify-center text-center">
                    <Clock className="h-5 w-5 text-emerald-400 mb-2" />
                    <p className="text-xs text-zinc-500 mb-1">Est. Duration</p>
                    <p className="text-lg font-semibold text-zinc-200">{workflow.estimated_duration}</p>
                  </motion.div>
                  <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.3 }} className="bg-zinc-950 border border-zinc-800 rounded-2xl p-4 shadow-xl flex flex-col items-center justify-center text-center">
                    <Coins className="h-5 w-5 text-amber-400 mb-2" />
                    <p className="text-xs text-zinc-500 mb-1">Est. Cost</p>
                    <p className="text-lg font-semibold text-zinc-200">{workflow.estimated_cost}</p>
                  </motion.div>
                  <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.4 }} className="bg-zinc-950 border border-amber-500/30 bg-amber-500/5 rounded-2xl p-4 shadow-xl flex flex-col items-center justify-center text-center">
                    <ShieldAlert className="h-5 w-5 text-amber-500 mb-2" />
                    <p className="text-xs text-zinc-500 mb-1">Human Approval</p>
                    <p className="text-lg font-semibold text-amber-500">{workflow.requires_human_approval ? 'Required' : 'None'}</p>
                  </motion.div>
                </>
              )}
            </AnimatePresence>
          </div>

          <div className="flex-1 bg-zinc-950 border border-zinc-800 rounded-2xl p-6 shadow-xl flex flex-col items-center justify-center relative overflow-hidden group">
            {/* Background Pattern */}
            <div className="absolute inset-0 opacity-20 pointer-events-none" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, rgba(255,255,255,0.15) 1px, transparent 0)', backgroundSize: '24px 24px' }}></div>
            
            <div className="z-10 text-center w-full max-w-lg">
              {!isReady ? (
                <div className="flex flex-col items-center justify-center">
                  <div className="h-16 w-16 bg-zinc-900 border border-zinc-800 rounded-2xl flex items-center justify-center mb-6 relative">
                    <div className="absolute inset-0 border-2 border-indigo-500/30 rounded-2xl animate-ping" />
                    <BrainCircuit className="h-8 w-8 text-indigo-400" />
                  </div>
                  <h3 className="text-xl font-medium text-zinc-200">AI is composing workflow</h3>
                  <p className="text-sm text-zinc-500 mt-2 h-6">
                    Generating dynamic graph via LLM capabilities...
                  </p>
                  
                  {/* Progress visualization */}
                  <div className="mt-8 flex items-center justify-center gap-4">
                    {[1, 2, 3].map((step) => (
                      <div key={step} className="flex items-center gap-4">
                        <motion.div 
                          initial={{ scale: 0.8, opacity: 0.5 }}
                          animate={{ 
                            scale: 1.1,
                            opacity: 1,
                            backgroundColor: '#6366f1'
                          }}
                          className="h-3 w-3 rounded-full"
                        />
                        {step < 3 && (
                          <motion.div 
                            initial={{ width: 0 }}
                            animate={{ width: 40 }}
                            className="h-0.5 bg-indigo-500/50"
                          />
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex flex-col items-center justify-center"
                >
                  <div className="h-20 w-20 bg-emerald-500/10 border border-emerald-500/30 rounded-full flex items-center justify-center mb-6">
                    <CheckCircle2 className="h-10 w-10 text-emerald-400" />
                  </div>
                  <h3 className="text-2xl font-semibold text-zinc-100">Execution Graph Ready</h3>
                  <p className="text-base text-zinc-400 mt-3 max-w-sm mx-auto leading-relaxed">
                    The AI has constructed a secure, {workflow?.nodes.length}-step plan using verified enterprise capabilities.
                  </p>
                </motion.div>
              )}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default function WorkflowPreviewPage() {
  return (
    <Suspense fallback={<div className="flex h-screen items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-cyan-500" /></div>}>
      <WorkflowPreviewContent />
    </Suspense>
  );
}
