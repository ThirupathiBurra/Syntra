"use client";

import { useRouter } from "next/navigation";

import { PageHeader } from "@/components/ui/PageHeader";
import { EmptyState } from "@/components/ui/EmptyState";
import { Box, Search, PlayCircle, Star, Clock, Workflow } from "lucide-react";
import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";

const WORKFLOW_TEMPLATES = [
  { id: "tmpl-1", name: "Employee Onboarding", category: "HR", runs: 1243, isOfficial: true },
  { id: "tmpl-2", name: "Vendor Contract Review", category: "Legal", runs: 892, isOfficial: true },
  { id: "tmpl-3", name: "Customer Complaint Escalation", category: "Support", runs: 412, isOfficial: false },
  { id: "tmpl-4", name: "Q3 Financial Reporting", category: "Finance", runs: 28, isOfficial: false },
];

export default function WorkflowStudioPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTab, setActiveTab] = useState("all");

  const filteredTemplates = WORKFLOW_TEMPLATES.filter(tmpl => {
    const matchesSearch = tmpl.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesTab = 
      activeTab === 'all' || 
      (activeTab === 'official' && tmpl.isOfficial) || 
      (activeTab === 'recent' && !tmpl.isOfficial); // Dummy logic for 'recent'
    return matchesSearch && matchesTab;
  });

  return (
    <div className="max-w-7xl mx-auto py-6 flex flex-col h-full">
      <PageHeader 
        title="Workflow Studio"
        description="Discover, manage, and execute dynamic AI orchestrations."
        icon={Workflow}
        action={
          <Link href="/" className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-lg shadow-indigo-500/20">
            <PlayCircle className="h-4 w-4" />
            Compose New
          </Link>
        }
      />

      <div className="flex-1 flex flex-col lg:flex-row gap-8">
        
        {/* Sidebar Nav */}
        <div className="w-full lg:w-64 flex-shrink-0 space-y-1">
          <button onClick={() => setActiveTab('all')} className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTab === 'all' ? "bg-indigo-500/10 text-indigo-400" : "text-zinc-400 hover:bg-zinc-900/50"}`}>
            <Box className="h-4 w-4" /> All Workflows
          </button>
          <button onClick={() => setActiveTab('official')} className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTab === 'official' ? "bg-indigo-500/10 text-indigo-400" : "text-zinc-400 hover:bg-zinc-900/50"}`}>
            <Star className="h-4 w-4" /> Official Templates
          </button>
          <button onClick={() => setActiveTab('recent')} className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTab === 'recent' ? "bg-indigo-500/10 text-indigo-400" : "text-zinc-400 hover:bg-zinc-900/50"}`}>
            <Clock className="h-4 w-4" /> Recently Generated
          </button>
        </div>

        {/* Content Area */}
        <div className="flex-1 bg-zinc-950 border border-zinc-800 rounded-2xl overflow-hidden flex flex-col shadow-xl">
          <div className="p-4 border-b border-zinc-800 bg-zinc-900/50 backdrop-blur-md">
            <div className="relative max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-500" />
              <input 
                type="text" 
                placeholder="Search workflows..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-zinc-950 border border-zinc-800 rounded-lg pl-9 pr-4 py-2 text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:border-indigo-500/50"
              />
            </div>
          </div>

          <div className="flex-1 p-6 overflow-auto">
            {filteredTemplates.length === 0 ? (
              <EmptyState title="No workflows found" description="Try searching for something else or compose a new workflow." icon={Workflow} />
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                {filteredTemplates.map((tmpl, idx) => (
                  <motion.div 
                    key={tmpl.id}
                    onClick={() => router.push(`/workflows/preview?q=Generate a workflow for ${encodeURIComponent(tmpl.name)}`)}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="group relative bg-zinc-900/40 border border-zinc-800 rounded-xl p-5 hover:bg-zinc-800/50 transition-all cursor-pointer"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div className="p-2 bg-zinc-950 border border-zinc-800 rounded-lg text-indigo-400 group-hover:scale-110 transition-transform">
                        <Workflow className="h-5 w-5" />
                      </div>
                      {tmpl.isOfficial && (
                        <span className="text-[10px] font-bold uppercase tracking-wider text-amber-500 bg-amber-500/10 px-2 py-0.5 rounded-full">Official</span>
                      )}
                    </div>
                    <h3 className="text-base font-semibold text-zinc-200 mb-1">{tmpl.name}</h3>
                    <div className="flex items-center gap-3 text-xs text-zinc-500">
                      <span>{tmpl.category}</span>
                      <span>•</span>
                      <span>{tmpl.runs.toLocaleString()} runs</span>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
