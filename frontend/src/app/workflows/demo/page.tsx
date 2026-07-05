"use client";

import { useEffect, useState } from "react";
import { BrainCircuit, ShieldAlert, Sparkles, Fingerprint } from "lucide-react";
import { DAGViewer } from "@/components/workflow/DAGViewer";
import { ExecutionTimeline } from "@/components/workflow/ExecutionTimeline";
import { motion } from "framer-motion";
import { eventStream } from "@/lib/api/sse";
import { formatSimpleMarkdown } from "@/lib/formatMarkdown";

export default function DemoWorkflow() {
  const [documents, setDocuments] = useState<Record<string, string> | null>(null);
  const [approvalRequested, setApprovalRequested] = useState<any>(null);
  const [isApproving, setIsApproving] = useState(false);
  const [isApproved, setIsApproved] = useState(false);
  const [typedDocs, setTypedDocs] = useState<Record<string, string>>({});

  useEffect(() => {
    eventStream.connect();
    
    const unsubscribeStarted = eventStream.on("WorkflowStarted", (data) => {
      console.log("Real-time Event: WorkflowStarted", data);
    });

    const unsubscribeCompleted = eventStream.on("NodeCompleted", (data) => {
      console.log("Real-time Event: NodeCompleted", data);
    });

    const unsubscribeApproval = eventStream.on("ApprovalRequested", (data: unknown) => {
      console.log("Real-time Event: ApprovalRequested", data);
      setApprovalRequested(data);
      const approvalData = data as { generated_documents?: Record<string, string> };
      if (approvalData?.generated_documents) {
        setDocuments(approvalData.generated_documents);
      }
    });

    return () => {
      unsubscribeStarted();
      unsubscribeCompleted();
      unsubscribeApproval();
      eventStream.disconnect();
    };
  }, []);

  // Simulate streaming text effect for documents
  useEffect(() => {
    if (!documents) return;
    
    const keys = Object.keys(documents);
    let currentKeyIdx = 0;
    let currentCharIdx = 0;
    
    setTypedDocs({}); // Reset
    
    const interval = setInterval(() => {
      if (currentKeyIdx >= keys.length) {
        clearInterval(interval);
        return;
      }
      
      const key = keys[currentKeyIdx];
      const fullText = documents[key];
      
      setTypedDocs(prev => ({
        ...prev,
        [key]: fullText.substring(0, currentCharIdx + 1)
      }));
      
      currentCharIdx += 5; // Type 5 chars at a time for speed
      
      if (currentCharIdx >= fullText.length) {
        currentKeyIdx++;
        currentCharIdx = 0;
      }
    }, 20);
    
    return () => clearInterval(interval);
  }, [documents]);

  return (
    <div className="flex h-full flex-col lg:flex-row gap-6 max-w-7xl mx-auto py-6">
      
      {/* Left Column: Workflow Context & Graph */}
      <div className="flex-1 flex flex-col gap-6">
        
        {/* Mission Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6 backdrop-blur-md"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="inline-flex items-center rounded-full border border-indigo-500/30 bg-indigo-500/10 px-2.5 py-0.5 text-xs font-semibold text-indigo-400">
              <Sparkles className="mr-1 h-3 w-3" />
              Active Mission
            </div>
            <span className="text-xs font-mono text-zinc-500">Session ID: exec-{(approvalRequested as { session_id?: string })?.session_id || "demo"}</span>
          </div>
          <h1 className="text-2xl font-semibold tracking-tight text-zinc-100">Workflow Execution</h1>
          <p className="text-sm text-zinc-400 mt-1">
            Running business orchestration logic based on retrieved enterprise knowledge.
          </p>
        </motion.div>

        {/* DAG Viewer */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="flex flex-col gap-2"
        >
          <h2 className="text-sm font-medium tracking-widest text-zinc-500 uppercase px-1">Execution Graph</h2>
          <DAGViewer />
        </motion.div>
        
        {/* Artifact/Insights Viewer */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="flex-1 rounded-2xl border border-zinc-800 bg-zinc-950 p-6 shadow-xl overflow-y-auto max-h-[500px]"
        >
          <div className="flex items-center gap-2 mb-4 pb-4 border-b border-zinc-800">
            <BrainCircuit className="h-5 w-5 text-indigo-400" />
            <h3 className="text-lg font-medium text-zinc-200">Generated Artifacts</h3>
          </div>
          
          <div className="space-y-6 text-sm text-zinc-300 leading-relaxed">
            {!documents ? (
              <div className="space-y-4">
                <div className="animate-pulse bg-zinc-900 h-4 w-3/4 rounded"></div>
                <div className="animate-pulse bg-zinc-900 h-4 w-full rounded"></div>
                <div className="animate-pulse bg-zinc-900 h-4 w-5/6 rounded"></div>
              </div>
            ) : (
              Object.entries(typedDocs).map(([key, content], idx) => (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  key={idx} 
                  className="p-4 rounded-xl border border-zinc-800 bg-zinc-900/50 shadow-inner"
                >
                   <h4 className="font-semibold text-zinc-100 mb-2 capitalize flex items-center gap-2">
                      {key.replace("_", " ")}
                      {content.length < documents[key].length && (
                        <span className="inline-block h-2 w-2 rounded-full bg-indigo-500 animate-pulse" />
                      )}
                   </h4>
                   <pre className="whitespace-pre-wrap font-sans text-zinc-400 text-xs">{content}</pre>
                </motion.div>
              ))
            )}
          </div>
        </motion.div>
      </div>

      {/* Right Column: Telemetry & Knowledge */}
      <motion.div 
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.3 }}
        className="w-full lg:w-96 flex flex-col gap-6"
      >
        
        {/* Timeline Panel */}
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900/40 p-5 backdrop-blur-md shadow-xl">
          <h2 className="text-sm font-medium tracking-widest text-zinc-500 uppercase mb-6">Mission Timeline</h2>
          <ExecutionTimeline />
        </div>

        {/* Explainability / Confidence Panel */}
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900/40 p-5 backdrop-blur-md shadow-xl">
           <h2 className="text-sm font-medium tracking-widest text-zinc-500 uppercase mb-4">Explainability & Confidence</h2>
           
           <div className="space-y-4">
              <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-4 transition-colors hover:border-cyan-500/30">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-cyan-400 flex items-center">
                    <Fingerprint className="w-4 h-4 mr-2" />
                    Knowledge Trace
                  </span>
                  <span className="text-xs font-mono text-cyan-500/70 bg-cyan-500/10 px-2 py-0.5 rounded-full">Retrieval</span>
                </div>
                <p className="text-xs text-zinc-400 leading-relaxed">
                  Data sourced from Enterprise Knowledge base and routed to generation engines securely.
                </p>
              </div>

              {Boolean(approvalRequested) && (
                <motion.div 
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-5 shadow-lg shadow-amber-500/10 relative overflow-hidden group"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-amber-500/5 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]" />
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-sm font-semibold text-amber-400 flex items-center">
                      <ShieldAlert className="w-4 h-4 mr-2" />
                      Human Approval Required
                    </span>
                  </div>
                  <div className="max-h-52 overflow-y-auto pr-2 mb-4 scrollbar-thin scrollbar-thumb-amber-500/20 scrollbar-track-transparent">
                    <p 
                      className="text-sm text-zinc-300 leading-relaxed"
                      dangerouslySetInnerHTML={{ 
                        __html: formatSimpleMarkdown((approvalRequested as { summary?: string })?.summary || "The workflow has paused and is waiting for your approval to proceed.") 
                      }}
                    />
                  </div>
                  <button 
                    onClick={() => {
                      setIsApproving(true);
                      setTimeout(() => {
                        setIsApproving(false);
                        setIsApproved(true);
                        // Dismiss the approval card after a short delay
                        setTimeout(() => setApprovalRequested(null), 1500);
                      }, 1000);
                    }}
                    disabled={isApproving || isApproved}
                    className={`w-full py-2.5 rounded-lg font-semibold text-sm transition-all shadow-md active:scale-95 flex items-center justify-center gap-2 ${
                      isApproved 
                        ? "bg-emerald-500 text-emerald-950 hover:bg-emerald-400" 
                        : "bg-amber-500 hover:bg-amber-400 text-zinc-950"
                    }`}
                  >
                    {isApproving ? (
                      <><span className="w-4 h-4 border-2 border-zinc-950 border-t-transparent rounded-full animate-spin"></span> Approving...</>
                    ) : isApproved ? (
                      <>Approved</>
                    ) : (
                      <>Review & Approve</>
                    )}
                  </button>
                </motion.div>
              )}
           </div>
        </div>

      </motion.div>
    </div>
  );
}
