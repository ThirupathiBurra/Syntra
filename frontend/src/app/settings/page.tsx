"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { Settings, Palette, Users, Database, Shield, Bell, Cpu, Key, ChevronRight, Check } from "lucide-react";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTheme } from "next-themes";

const SETTINGS_SECTIONS = [
  { id: "appearance", label: "Appearance", icon: Palette },
  { id: "workspace", label: "Workspace", icon: Database },
  { id: "users", label: "Users & Roles", icon: Users },
  { id: "ai_models", label: "AI Models", icon: Cpu },
  { id: "security", label: "Security", icon: Shield },
  { id: "notifications", label: "Notifications", icon: Bell },
  { id: "api_keys", label: "API Keys", icon: Key },
];

function SettingRow({ label, description, children }: { label: string; description?: string; children: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between py-4 border-b border-zinc-100 dark:border-zinc-800/60 last:border-0">
      <div className="flex-1 pr-8">
        <p className="text-sm font-medium text-zinc-900 dark:text-zinc-100">{label}</p>
        {description && <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">{description}</p>}
      </div>
      <div className="flex-shrink-0">{children}</div>
    </div>
  );
}

function Toggle({ enabled, onChange }: { enabled: boolean; onChange: () => void }) {
  return (
    <button
      onClick={onChange}
      className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${enabled ? "bg-indigo-600" : "bg-zinc-300 dark:bg-zinc-700"}`}
    >
      <span className={`inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow-sm transition-transform ${enabled ? "translate-x-5" : "translate-x-1"}`} />
    </button>
  );
}

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState("appearance");
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [notif, setNotif] = useState({ email: true, slack: false, approvals: true, failures: true });
  const [sec, setSec] = useState({ hitl: true, auditLog: true, mfa: false });
  const [saved, setSaved] = useState(false);

  useEffect(() => { setMounted(true); }, []);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="max-w-6xl mx-auto py-6 flex flex-col h-full">
      <div className="flex items-center justify-between mb-8">
        <PageHeader title="Settings" description="Configure workspace, security, and AI execution preferences." icon={Settings} />
        <button onClick={handleSave} className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${saved ? "bg-emerald-500/10 text-emerald-500 border border-emerald-500/30" : "bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-500/20"}`}>
          {saved ? <><Check className="h-4 w-4" /> Saved!</> : "Save Changes"}
        </button>
      </div>

      <div className="flex-1 flex flex-col md:flex-row gap-8">
        <div className="w-full md:w-52 flex-shrink-0 space-y-0.5">
          {SETTINGS_SECTIONS.map((section) => (
            <button key={section.id} onClick={() => setActiveSection(section.id)} className={`w-full flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeSection === section.id ? "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400" : "text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-900/50 hover:text-zinc-900 dark:hover:text-zinc-200"}`}>
              <div className="flex items-center gap-3"><section.icon className="h-4 w-4" />{section.label}</div>
              {activeSection === section.id && <ChevronRight className="h-3 w-3" />}
            </button>
          ))}
        </div>

        <div className="flex-1 min-w-0">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.15 }}>

              {activeSection === "appearance" && mounted && (
                <div className="bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 shadow-sm">
                  <h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100 mb-1">Theme</h3>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-5">Choose the display theme for the Syntra OS interface.</p>
                  <div className="grid grid-cols-3 gap-4">
                    {(["light", "dark", "system"] as const).map((t) => (
                      <button key={t} onClick={() => setTheme(t)} className={`flex flex-col items-center p-4 rounded-xl border-2 transition-all ${theme === t ? "border-indigo-500 bg-indigo-50 dark:bg-indigo-500/10" : "border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700"}`}>
                        <div className={`w-full h-14 rounded-lg mb-3 border overflow-hidden flex ${t === "light" ? "bg-white border-zinc-200" : t === "dark" ? "bg-zinc-950 border-zinc-800" : "border-zinc-200 dark:border-zinc-800"}`}>
                          {t === "system" && <><div className="w-1/2 h-full bg-white" /><div className="w-1/2 h-full bg-zinc-950" /></>}
                        </div>
                        <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 capitalize">{t}</span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {activeSection === "workspace" && (
                <div className="bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 shadow-sm space-y-5">
                  <div><h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100 mb-1">Workspace Configuration</h3><p className="text-sm text-zinc-500 dark:text-zinc-400">Configure your enterprise workspace name and default behavior.</p></div>
                  <div><label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">Workspace Name</label><input defaultValue="Enterprise Workspace" className="w-full bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-lg px-3 py-2 text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-1 focus:ring-indigo-500/50" /></div>
                  <div><label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">Default Department</label><select className="w-full bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-lg px-3 py-2 text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none"><option>Operations</option><option>Engineering</option><option>Legal</option><option>Finance</option><option>HR</option></select></div>
                  <SettingRow label="Require Approval on All Workflows" description="Pause every workflow before execution for human review."><Toggle enabled={false} onChange={() => {}} /></SettingRow>
                </div>
              )}

              {activeSection === "users" && (
                <div className="bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-2xl overflow-hidden shadow-sm">
                  <div className="px-6 py-5 border-b border-zinc-100 dark:border-zinc-800"><h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">Team Members</h3><p className="text-sm text-zinc-500 dark:text-zinc-400 mt-0.5">Manage user access and roles for this workspace.</p></div>
                  <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
                    {[{name:"System Admin",email:"admin@company.com",role:"Owner",av:"SA"},{name:"Sarah Chen",email:"s.chen@company.com",role:"Editor",av:"SC"},{name:"James Patel",email:"j.patel@company.com",role:"Viewer",av:"JP"}].map((u)=>(
                      <div key={u.email} className="flex items-center justify-between px-6 py-4">
                        <div className="flex items-center gap-3"><div className="h-8 w-8 rounded-full bg-indigo-600/10 border border-indigo-500/20 flex items-center justify-center text-xs font-bold text-indigo-500">{u.av}</div><div><p className="text-sm font-medium text-zinc-900 dark:text-zinc-100">{u.name}</p><p className="text-xs text-zinc-500">{u.email}</p></div></div>
                        <span className={`text-[11px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${u.role==="Owner"?"text-amber-500 bg-amber-500/10":u.role==="Editor"?"text-indigo-500 bg-indigo-500/10":"text-zinc-500 bg-zinc-100 dark:bg-zinc-800"}`}>{u.role}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeSection === "ai_models" && (
                <div className="bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 shadow-sm space-y-5">
                  <div><h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100 mb-1">AI Model Configuration</h3><p className="text-sm text-zinc-500 dark:text-zinc-400">Select which LLM powers each stage of the execution pipeline.</p></div>
                  {[{label:"Planner & Orchestrator",val:"Gemini 2.5 Flash"},{label:"Knowledge Retrieval (Embeddings)",val:"text-embedding-3-small"},{label:"Document Generation Agent",val:"Gemini 2.5 Flash"}].map((m)=>(
                    <div key={m.label}><label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">{m.label}</label><select className="w-full bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-lg px-3 py-2 text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none"><option>{m.val}</option><option>GPT-4o</option><option>Claude 3.5 Sonnet</option></select></div>
                  ))}
                </div>
              )}

              {activeSection === "security" && (
                <div className="bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 shadow-sm">
                  <h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100 mb-1">Security & Compliance</h3>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-5">Control access, audit trails, and execution guardrails.</p>
                  <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
                    <SettingRow label="Human-in-the-Loop Enforcement" description="Force human approval before all high-risk agent actions."><Toggle enabled={sec.hitl} onChange={() => setSec(s=>({...s,hitl:!s.hitl}))} /></SettingRow>
                    <SettingRow label="Audit Log Retention" description="Retain execution audit logs for compliance review."><Toggle enabled={sec.auditLog} onChange={() => setSec(s=>({...s,auditLog:!s.auditLog}))} /></SettingRow>
                    <SettingRow label="Multi-Factor Authentication" description="Require MFA for all admin workspace actions."><Toggle enabled={sec.mfa} onChange={() => setSec(s=>({...s,mfa:!s.mfa}))} /></SettingRow>
                  </div>
                </div>
              )}

              {activeSection === "notifications" && (
                <div className="bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 shadow-sm">
                  <h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100 mb-1">Notification Preferences</h3>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-5">Choose how and when you receive alerts from the AI workforce.</p>
                  <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
                    <SettingRow label="Email Notifications" description="Receive workflow completion summaries by email."><Toggle enabled={notif.email} onChange={() => setNotif(s=>({...s,email:!s.email}))} /></SettingRow>
                    <SettingRow label="Slack Integration" description="Post workflow results and approval requests to Slack."><Toggle enabled={notif.slack} onChange={() => setNotif(s=>({...s,slack:!s.slack}))} /></SettingRow>
                    <SettingRow label="Approval Alerts" description="Get notified when a workflow requires your approval."><Toggle enabled={notif.approvals} onChange={() => setNotif(s=>({...s,approvals:!s.approvals}))} /></SettingRow>
                    <SettingRow label="Failure Alerts" description="Get notified when a workflow fails or encounters an error."><Toggle enabled={notif.failures} onChange={() => setNotif(s=>({...s,failures:!s.failures}))} /></SettingRow>
                  </div>
                </div>
              )}

              {activeSection === "api_keys" && (
                <div className="bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-2xl overflow-hidden shadow-sm">
                  <div className="px-6 py-5 border-b border-zinc-100 dark:border-zinc-800"><h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">API Keys</h3><p className="text-sm text-zinc-500 dark:text-zinc-400 mt-0.5">Manage API keys for external integrations and developer access.</p></div>
                  <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
                    {[{label:"Syntra API Key",key:"syn_live_••••••••••••7k2a"},{label:"Webhook Secret",key:"whsec_••••••••••••9mp1"}].map((k)=>(
                      <div key={k.label} className="px-6 py-4 flex items-center justify-between"><div><p className="text-sm font-medium text-zinc-900 dark:text-zinc-100">{k.label}</p><p className="text-xs font-mono text-zinc-500 mt-0.5">{k.key}</p></div><span className="text-[11px] font-bold uppercase tracking-wider text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded-full">Active</span></div>
                    ))}
                  </div>
                  <div className="px-6 py-4 bg-zinc-50 dark:bg-zinc-900/50"><button className="text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-500">+ Generate New API Key</button></div>
                </div>
              )}

            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
