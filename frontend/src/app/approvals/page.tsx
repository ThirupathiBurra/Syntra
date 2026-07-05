"use client";

import { PageHeader } from "@/components/ui/PageHeader";

import { EmptyState } from "@/components/ui/EmptyState";
import { CheckSquare, Search, ShieldAlert, FileText, Check, X } from "lucide-react";
import { useState } from "react";

import Link from "next/link";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

interface Approval {
  approval_id: string;
  workflow_id: string;
  node_id: string;
  workflow_name?: string;
  status: string;
  summary: string;
  created_at: string;
}

const fetchApprovals = async (): Promise<Approval[]> => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/approvals`);
  if (!res.ok) throw new Error("Failed to fetch approvals");
  return res.json();
};

const resolveApproval = async ({ id, action }: { id: string; action: "approve" | "reject" }) => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/approvals/${id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ action }),
  });
  if (!res.ok) throw new Error("Failed to resolve approval");
  return res.json();
};

export default function ApprovalsPage() {
  const queryClient = useQueryClient();
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const { data: approvals = [], isLoading } = useQuery({
    queryKey: ["approvals"],
    queryFn: fetchApprovals,
  });

  const resolveMutation = useMutation({
    mutationFn: resolveApproval,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["approvals"] });
      setSelectedId(null);
    }
  });

  const filteredApprovals = approvals.filter(apprv => 
    (apprv.workflow_name || apprv.workflow_id).toLowerCase().includes(searchQuery.toLowerCase())
  );

  const selectedApproval = approvals.find(a => a.approval_id === selectedId) || null;

  return (
    <div className="max-w-7xl mx-auto py-6 flex flex-col h-full">
      <PageHeader 
        title="Human-in-the-Loop Approvals"
        description="Review and action workflows that require explicit human authorization."
        icon={CheckSquare}
      />

      <div className="flex-1 flex flex-col lg:flex-row gap-6 overflow-hidden">
        
        {/* Left Column: Task List */}
        <div className="w-full lg:w-1/3 flex flex-col bg-zinc-950 border border-zinc-800 rounded-2xl shadow-xl overflow-hidden">
          <div className="p-4 border-b border-zinc-800 bg-zinc-900/50 backdrop-blur-md">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-500" />
              <input 
                type="text" 
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-zinc-950 border border-zinc-800 rounded-lg pl-9 pr-4 py-2 text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:border-indigo-500/50"
              />
            </div>
          </div>
          <div className="flex-1 overflow-auto p-2">
            {isLoading ? (
              <div className="p-8 text-center text-zinc-500 text-sm">Loading approvals...</div>
            ) : filteredApprovals.length === 0 ? (
              <EmptyState title="No pending approvals" description="All caught up!" icon={CheckSquare} />
            ) : (
              <div className="space-y-2">
                {filteredApprovals.map((apprv) => (
                  <button 
                    key={apprv.approval_id}
                    onClick={() => setSelectedId(apprv.approval_id)}
                    className={`w-full text-left p-4 rounded-xl border transition-all ${selectedId === apprv.approval_id ? 'bg-indigo-500/10 border-indigo-500/30' : 'bg-zinc-900/30 border-transparent hover:bg-zinc-900/50'}`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-xs font-mono text-zinc-500">{apprv.approval_id.slice(0, 8)}</span>
                      <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-500">
                        Pending
                      </span>
                    </div>
                    <h4 className="text-sm font-semibold text-zinc-200 mb-1">{apprv.workflow_name || apprv.workflow_id}</h4>
                    <p className="text-xs text-zinc-500">{new Date(apprv.created_at).toLocaleString()}</p>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Task Details */}
        <div className="flex-1 bg-zinc-950 border border-zinc-800 rounded-2xl shadow-xl overflow-hidden flex flex-col">
          {selectedApproval ? (
            <>
              <div className="p-6 border-b border-zinc-800 bg-zinc-900/20">
                <div className="flex items-center gap-3 mb-4">
                  <ShieldAlert className="h-6 w-6 text-amber-500" />
                  <h2 className="text-xl font-semibold text-zinc-100">{selectedApproval.workflow_name || selectedApproval.workflow_id}</h2>
                </div>
                <p className="text-sm text-zinc-400 mb-6">
                  Workflow <Link href={`/workflows/${selectedApproval.workflow_id}`} className="text-indigo-400 hover:underline font-mono">{selectedApproval.workflow_id.slice(0, 8)}</Link> is paused and requires your approval.
                </p>
                <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-4">
                  <h3 className="text-sm font-medium text-amber-500 mb-2">AI Summary</h3>
                  <p className="text-sm text-zinc-300 leading-relaxed">{selectedApproval.summary}</p>
                </div>
              </div>
              
              <div className="flex-1 overflow-auto p-6">
                <h3 className="text-sm font-medium tracking-widest text-zinc-500 uppercase mb-4">Generated Documents</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {(selectedApproval as { documents?: string[] }).documents?.map((doc: string, idx: number) => (
                    <div key={idx} className="flex items-center gap-3 p-4 rounded-xl border border-zinc-800 bg-zinc-900/30">
                      <FileText className="h-8 w-8 text-zinc-500" />
                      <div>
                        <p className="text-sm font-medium text-zinc-200">{doc}</p>
                        <p className="text-xs text-zinc-500 cursor-pointer hover:text-indigo-400">View Content</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="p-6 border-t border-zinc-800 bg-zinc-900/50 flex items-center justify-end gap-4">
                <button 
                  onClick={() => resolveMutation.mutate({ id: selectedApproval.approval_id, action: "reject" })}
                  disabled={resolveMutation.isPending}
                  className="inline-flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-medium text-zinc-300 hover:text-white bg-zinc-800 hover:bg-zinc-700 transition-colors disabled:opacity-50"
                >
                  <X className="h-4 w-4" />
                  Reject
                </button>
                <button 
                  onClick={() => resolveMutation.mutate({ id: selectedApproval.approval_id, action: "approve" })}
                  disabled={resolveMutation.isPending}
                  className="inline-flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-500/20 transition-all disabled:opacity-50"
                >
                  <Check className="h-4 w-4" />
                  Approve & Continue
                </button>
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <EmptyState title="Select a task" description="Choose an approval task from the sidebar to view details." icon={CheckSquare} />
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
