"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { StatusBadge, StatusType } from "@/components/ui/StatusBadge";
import { EmptyState } from "@/components/ui/EmptyState";
import { Activity, Search, Filter, MoreVertical, PlayCircle } from "lucide-react";
import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";

interface Workflow {
  workflow_id: string;
  name: string;
  status?: StatusType;
  department: string;
  created_at: string;
}

const fetchWorkflows = async (): Promise<Workflow[]> => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/workflows`);
  if (!res.ok) throw new Error("Failed to fetch workflows");
  return res.json();
};

export default function ActiveWorkflowsPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [showFilters, setShowFilters] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);

  const { data: workflows = [], isLoading, error } = useQuery({
    queryKey: ["workflows"],
    queryFn: fetchWorkflows,
  });

  const filteredWorkflows = workflows.filter(wf => 
    wf.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    wf.workflow_id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto py-6 flex flex-col h-full">
      <PageHeader 
        title="Active Workflows"
        description="Monitor running business orchestrations and view execution history."
        icon={Activity}
        action={
          <Link href="/" className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            <PlayCircle className="h-4 w-4" />
            New Workflow
          </Link>
        }
      />

      <div className="flex-1 bg-zinc-950 border border-zinc-800 rounded-2xl overflow-hidden flex flex-col shadow-xl">
        {/* Toolbar */}
        <div className="p-4 border-b border-zinc-800 flex items-center justify-between gap-4 bg-zinc-900/50 backdrop-blur-md">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-500" />
            <input 
              type="text" 
              placeholder="Search by mission name or session ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-lg pl-9 pr-4 py-2 text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all"
            />
          </div>
          <button 
            onClick={() => setShowFilters(!showFilters)}
            className={`inline-flex items-center gap-2 px-3 py-2 text-sm rounded-md transition-colors ${
              showFilters ? "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20" : "text-zinc-300 hover:text-white hover:bg-zinc-800 border border-transparent"
            }`}
          >
            <Filter className="h-4 w-4" />
            Filters
          </button>
        </div>

        {/* Dummy Filter Expansion */}
        {showFilters && (
          <div className="px-4 py-3 border-b border-zinc-800/50 bg-zinc-900/30 flex gap-3 animate-in fade-in slide-in-from-top-2">
            <select className="bg-zinc-950 border border-zinc-800 rounded-md px-3 py-1 text-sm text-zinc-300 focus:outline-none focus:border-indigo-500/50">
              <option>All Statuses</option>
              <option>Running</option>
              <option>Completed</option>
              <option>Failed</option>
            </select>
            <select className="bg-zinc-950 border border-zinc-800 rounded-md px-3 py-1 text-sm text-zinc-300 focus:outline-none focus:border-indigo-500/50">
              <option>All Departments</option>
              <option>HR</option>
              <option>Engineering</option>
              <option>Finance</option>
            </select>
          </div>
        )}

        {/* Data Table */}
        <div className="flex-1 overflow-auto">
          {isLoading ? (
            <div className="p-8 text-center text-zinc-400">Loading workflows...</div>
          ) : error ? (
            <div className="p-8 text-center text-red-400">Error loading workflows</div>
          ) : filteredWorkflows.length === 0 ? (
            <div className="p-8">
              <EmptyState 
                title="No workflows found" 
                description="Try adjusting your search query or starting a new mission."
                icon={Activity}
              />
            </div>
          ) : (
            <table className="w-full text-left text-sm text-zinc-400">
              <thead className="bg-zinc-900/50 text-xs uppercase font-medium text-zinc-500 sticky top-0 backdrop-blur-md z-10">
                <tr>
                  <th className="px-6 py-4 rounded-tl-xl">Session ID</th>
                  <th className="px-6 py-4">Mission Name</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4 hidden lg:table-cell">Duration</th>
                  <th className="px-6 py-4 hidden md:table-cell">Initiator</th>
                  <th className="px-6 py-4 text-right rounded-tr-xl"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/50">
                {filteredWorkflows.map((wf, idx) => (
                    <motion.tr 
                      key={wf.workflow_id}
                      onClick={() => router.push(`/workflows/demo`)}
                      initial={{ opacity: 0, y: 5 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.05 }}
                      className="hover:bg-zinc-900/30 transition-colors group cursor-pointer"
                    >
                      <td className="px-6 py-4 font-mono text-xs text-zinc-500">{wf.workflow_id.slice(0, 8)}</td>
                      <td className="px-6 py-4 font-medium text-zinc-200">{wf.name}</td>
                      <td className="px-6 py-4">
                        <StatusBadge status={wf.status || "completed"} />
                        {wf.status === "running" && (
                          <div className="mt-2 h-1 w-24 bg-zinc-800 rounded-full overflow-hidden">
                            <motion.div 
                              className="h-full bg-indigo-500" 
                              initial={{ width: "0%" }}
                              animate={{ width: "65%" }}
                              transition={{ duration: 2, ease: "easeOut" }}
                            />
                          </div>
                        )}
                      </td>
                      <td className="px-6 py-4 hidden lg:table-cell text-zinc-500">-</td>
                      <td className="px-6 py-4 hidden md:table-cell text-zinc-400">{wf.department}</td>
                      <td className="px-6 py-4 text-right relative">
                        <button 
                          onClick={(e) => {
                            e.stopPropagation();
                            setActiveDropdown(activeDropdown === wf.workflow_id ? null : wf.workflow_id);
                          }}
                          className={`p-1 rounded transition-opacity ${
                            activeDropdown === wf.workflow_id 
                              ? "text-zinc-100 bg-zinc-800 opacity-100" 
                              : "text-zinc-600 hover:text-zinc-300 opacity-0 group-hover:opacity-100"
                          }`}
                        >
                          <MoreVertical className="h-4 w-4" />
                        </button>
                        
                        {activeDropdown === wf.workflow_id && (
                          <div className="absolute right-6 top-10 mt-1 w-32 bg-zinc-900 border border-zinc-700 rounded-lg shadow-xl overflow-hidden z-50 animate-in fade-in zoom-in-95">
                            <button className="w-full text-left px-3 py-2 text-sm text-zinc-300 hover:bg-zinc-800 hover:text-white transition-colors">
                              View Details
                            </button>
                            <button className="w-full text-left px-3 py-2 text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-colors">
                              Cancel Run
                            </button>
                          </div>
                        )}
                      </td>
                    </motion.tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
