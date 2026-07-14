"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { LayoutDashboard, Compass, Database, CheckSquare, Settings, Activity, PanelLeftClose, PanelLeftOpen, BarChart2, Workflow } from "lucide-react";

export function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const pathname = usePathname();

  const navItems = [
    { name: "Mission Control", href: "/", icon: LayoutDashboard },
    { name: "Analytics", href: "/analytics", icon: BarChart2 },
    { name: "Workflow Studio", href: "/studio", icon: Workflow },
    { name: "Knowledge Base", href: "/knowledge", icon: Database },
    { name: "Active Workflows", href: "/workflows", icon: Activity },
    { name: "Approvals", href: "/approvals", icon: CheckSquare },
    { name: "Settings", href: "/settings", icon: Settings },
  ];

  const isActive = (href: string) => {
    if (href === "/") return pathname === "/";
    return pathname.startsWith(href);
  };

  return (
    <aside className={`${isCollapsed ? 'w-16' : 'w-64'} border-r border-zinc-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-950/50 backdrop-blur-xl hidden md:flex flex-col h-full transition-all duration-300 relative group`}>
      <button 
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute -right-3 top-4 h-6 w-6 bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700 rounded-full flex items-center justify-center text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 opacity-0 group-hover:opacity-100 transition-opacity z-50"
      >
        {isCollapsed ? <PanelLeftOpen className="h-3 w-3" /> : <PanelLeftClose className="h-3 w-3" />}
      </button>

      <div className="flex h-14 items-center px-4 border-b border-zinc-200 dark:border-zinc-800/50 overflow-hidden">
        <Compass className="h-6 w-6 text-indigo-500 mr-2 flex-shrink-0" />
        <span className={`font-semibold text-lg tracking-tight text-zinc-900 dark:text-zinc-100 whitespace-nowrap transition-opacity duration-300 ${isCollapsed ? 'opacity-0 w-0 hidden' : 'opacity-100'}`}>Syntra OS</span>
      </div>
      
      <div className="flex-1 overflow-y-auto py-4 overflow-x-hidden">
        <nav className="space-y-1 px-2">
          {navItems.map((item) => (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                isActive(item.href)
                  ? "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20"
                  : "text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-50 hover:bg-zinc-100 dark:hover:bg-zinc-800/50"
              }`}
              title={item.name}
            >
              <item.icon className="mr-3 h-5 w-5 flex-shrink-0" aria-hidden="true" />
              <span className={`whitespace-nowrap transition-opacity duration-300 ${isCollapsed ? 'opacity-0 w-0 hidden' : 'opacity-100'}`}>{item.name}</span>
            </Link>
          ))}
        </nav>
      </div>
      
      <div className="p-4 border-t border-zinc-200 dark:border-zinc-800/50 overflow-hidden">
        <div className="flex items-center">
          <div className="h-8 w-8 rounded-full bg-indigo-600 flex items-center justify-center text-white font-medium text-sm shadow-lg shadow-indigo-500/20 flex-shrink-0">
            S
          </div>
          <div className={`ml-3 whitespace-nowrap transition-opacity duration-300 ${isCollapsed ? 'opacity-0 w-0 hidden' : 'opacity-100'}`}>
            <p className="text-sm font-medium text-zinc-900 dark:text-zinc-200">System Admin</p>
            <p className="text-xs font-medium text-zinc-500">Enterprise Workspace</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
