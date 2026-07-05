"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { StatusBadge, StatusType } from "@/components/ui/StatusBadge";
import { EmptyState } from "@/components/ui/EmptyState";
import { Layers, Upload, Search, Filter, MoreVertical, FileText } from "lucide-react";
import { useState, useRef } from "react";
import { motion } from "framer-motion";

import { useQuery, useQueryClient } from "@tanstack/react-query";

interface Document {
  document_id: string;
  name: string;
  type: string;
  owner: string;
  size: string;
  status: StatusType;
  created_at: string;
}

const fetchDocuments = async (): Promise<Document[]> => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/knowledge`);
  if (!res.ok) throw new Error("Failed to fetch documents");
  return res.json();
};

export default function KnowledgeBasePage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const queryClient = useQueryClient();

  const { data: documents = [], isLoading } = useQuery({
    queryKey: ["documents"],
    queryFn: fetchDocuments,
  });

  const filteredDocs = documents.filter(doc => 
    doc.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setIsUploading(true);
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/knowledge/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      // Clear the input so the same file can be uploaded again if needed
      if (fileInputRef.current) fileInputRef.current.value = "";
      
      // Refresh documents list
      queryClient.invalidateQueries({ queryKey: ["documents"] });
    } catch (error) {
      console.error("Error uploading document:", error);
      alert("Failed to upload document. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-6 flex flex-col h-full">
      <PageHeader 
        title="Knowledge Base"
        description="Manage and monitor enterprise documents indexed for AI workflows."
        icon={Layers}
        action={
          <>
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleFileUpload} 
              className="hidden" 
              accept=".txt,.pdf,.md,.csv,.json,text/plain"
            />
            <button 
              onClick={() => fileInputRef.current?.click()}
              disabled={isUploading}
              className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-600/50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              <Upload className={`h-4 w-4 ${isUploading ? 'animate-pulse' : ''}`} />
              {isUploading ? 'Uploading...' : 'Upload Documents'}
            </button>
          </>
        }
      />

      <div className="flex-1 bg-zinc-950 border border-zinc-800 rounded-2xl overflow-hidden flex flex-col shadow-xl">
        {/* Toolbar */}
        <div className="p-4 border-b border-zinc-800 flex items-center justify-between gap-4 bg-zinc-900/50 backdrop-blur-md">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-500" />
            <input 
              type="text" 
              placeholder="Search documents by name or content..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-lg pl-9 pr-4 py-2 text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all"
            />
          </div>
          <button className="inline-flex items-center gap-2 px-3 py-2 text-sm text-zinc-300 hover:text-white hover:bg-zinc-800 rounded-md transition-colors">
            <Filter className="h-4 w-4" />
            Filters
          </button>
        </div>

        {/* Data Table */}
        <div className="flex-1 overflow-auto">
          {isLoading ? (
            <div className="p-8 text-center text-zinc-500">Loading documents...</div>
          ) : filteredDocs.length === 0 ? (
            <div className="p-8">
              <EmptyState 
                title="No documents found" 
                description="Try adjusting your search query or uploading a new document."
                icon={FileText}
              />
            </div>
          ) : (
            <table className="w-full text-left text-sm text-zinc-400">
              <thead className="bg-zinc-900/50 text-xs uppercase font-medium text-zinc-500 sticky top-0 backdrop-blur-md">
                <tr>
                  <th className="px-6 py-4 rounded-tl-xl">Document Name</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4 hidden md:table-cell">Owner</th>
                  <th className="px-6 py-4 hidden lg:table-cell">Size</th>
                  <th className="px-6 py-4">Uploaded</th>
                  <th className="px-6 py-4 text-right rounded-tr-xl"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/50">
                {filteredDocs.map((doc, idx) => (
                  <motion.tr 
                    key={doc.document_id}
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="hover:bg-zinc-900/30 transition-colors group cursor-pointer"
                  >
                    <td className="px-6 py-4 font-medium text-zinc-200">
                      <div className="flex items-center gap-3">
                        <FileText className="h-4 w-4 text-zinc-500" />
                        {doc.name}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <StatusBadge status={doc.status} />
                    </td>
                    <td className="px-6 py-4 hidden md:table-cell text-zinc-400">{doc.owner}</td>
                    <td className="px-6 py-4 hidden lg:table-cell text-zinc-500">{doc.size}</td>
                    <td className="px-6 py-4 text-zinc-500">{new Date(doc.created_at).toLocaleString()}</td>
                    <td className="px-6 py-4 text-right">
                      <button className="p-1 text-zinc-600 hover:text-zinc-300 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                        <MoreVertical className="h-4 w-4" />
                      </button>
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
