"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { Settings, Users, Brain, Shield, Bell, Key, Palette, Cpu } from "lucide-react";
import { useState } from "react";
import { motion } from "framer-motion";

const SETTINGS_SECTIONS = [
  { id: "workspace", label: "Workspace", icon: Settings },
  { id: "users", label: "Users & Teams", icon: Users },
  { id: "ai", label: "AI Models", icon: Brain },
  { id: "security", label: "Security", icon: Shield },
  { id: "notifications", label: "Notifications", icon: Bell },
  { id: "api", label: "API Keys", icon: Key },
  { id: "appearance", label: "Appearance", icon: Palette },
  { id: "execution", label: "Execution Engine", icon: Cpu },
];

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState("ai");

  return (
    <div className="max-w-6xl mx-auto py-6 flex flex-col h-full">
      <PageHeader 
        title="Settings"
        description="Configure your enterprise workspace, AI models, and access controls."
        icon={Settings}
      />

      <div className="flex-1 flex flex-col md:flex-row gap-8">
        
        {/* Sidebar Nav */}
        <div className="w-full md:w-64 flex-shrink-0 space-y-1">
          {SETTINGS_SECTIONS.map((section) => (
            <button
              key={section.id}
              onClick={() => setActiveSection(section.id)}
              className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                activeSection === section.id 
                  ? "bg-indigo-500/10 text-indigo-400" 
                  : "text-zinc-400 hover:bg-zinc-900/50 hover:text-zinc-200"
              }`}
            >
              <section.icon className="h-4 w-4" />
              {section.label}
            </button>
          ))}
        </div>

        {/* Content Area */}
        <div className="flex-1">
          {activeSection === "ai" && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <div>
                <h3 className="text-lg font-medium text-zinc-100">AI Models</h3>
                <p className="text-sm text-zinc-400 mt-1">Configure default models for planning, execution, and embeddings.</p>
              </div>

              <div className="bg-zinc-950 border border-zinc-800 rounded-2xl overflow-hidden shadow-xl">
                <div className="p-6 space-y-6">
                  
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Default Planning Model</label>
                    <select disabled className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-2.5 text-sm text-zinc-400 appearance-none opacity-60 cursor-not-allowed">
                      <option>Gemini 2.5 Flash</option>
                      <option>Gemini 2.5 Pro</option>
                    </select>
                    <p className="mt-1 text-xs text-zinc-500">Used by the Conductor for complex reasoning and plan generation.</p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Default Generation Model</label>
                    <select disabled className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-2.5 text-sm text-zinc-400 appearance-none opacity-60 cursor-not-allowed">
                      <option>Gemini 2.5 Flash</option>
                      <option>Gemini 2.5 Pro</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Google Provider API Key</label>
                    <input 
                      type="password" 
                      value="************************"
                      disabled
                      className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-2.5 text-sm text-zinc-400 opacity-60 cursor-not-allowed"
                    />
                    <p className="mt-1 text-xs text-zinc-500">Configured via environment variables.</p>
                  </div>

                </div>
                <div className="p-4 border-t border-zinc-800 bg-zinc-900/30 flex justify-end">
                  <button disabled className="px-4 py-2 bg-zinc-800 text-zinc-500 rounded-lg text-sm font-medium cursor-not-allowed">
                    Save Changes
                  </button>
                </div>
              </div>
            </motion.div>
          )}

          {activeSection !== "ai" && (
            <div className="flex flex-col items-center justify-center py-24 text-center border border-dashed border-zinc-800 rounded-2xl bg-zinc-900/10">
              <Settings className="h-8 w-8 text-zinc-600 mb-4 animate-spin-slow" />
              <h3 className="text-lg font-medium text-zinc-300 capitalize">{activeSection} Settings</h3>
              <p className="mt-2 text-sm text-zinc-500 max-w-sm">This section is currently under construction for the enterprise preview.</p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
