import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { WelcomeModal } from "@/components/ui/WelcomeModal";
import { QueryProvider } from "@/components/providers/QueryProvider";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "Syntra | Enterprise AI OS",
  description: "Dynamic AI Workflow Orchestration",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} font-sans antialiased bg-zinc-950 text-zinc-50 overflow-hidden`}>
        <QueryProvider>
          <WelcomeModal />
          <div className="flex h-screen w-full">
            <Sidebar />
            <div className="flex-1 flex flex-col min-w-0">
              <Topbar />
              <main className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8">
                {children}
              </main>
            </div>
          </div>
        </QueryProvider>
      </body>
    </html>
  );
}
