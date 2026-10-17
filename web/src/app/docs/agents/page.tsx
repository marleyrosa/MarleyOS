"use client";

import Link from "next/link";
import { Lightbulb } from "lucide-react";
import agentsData from "@/services/agents.json";
import { useI18n } from "@/i18n/provider";

export default function AgentsPage() {
    const { t } = useI18n();
    const agents = agentsData;

    return (
        <div className="max-w-3xl">
            {/* Breadcrumb */}
            <nav className="flex items-center gap-2 text-sm text-muted-foreground mb-6">
                <Link href="/docs" className="hover:text-foreground">{t.agentsPage.breadcrumbDocs}</Link>
                <span>/</span>
                <span className="text-foreground">{t.agentsPage.breadcrumbCurrent}</span>
            </nav>

            {/* Page Header */}
            <div className="mb-8 pb-8 border-b border-border">
                <h1 className="text-4xl font-bold tracking-tight text-foreground mb-4">
                    {t.agentsPage.title}
                </h1>
                <p className="text-lg text-muted-foreground">
                    {t.agentsPage.subtitle}
                </p>
            </div>

            {/* What are Agents */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.agentsPage.whatTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-4">
                    {t.agentsPage.whatP1}
                </p>
                <p className="text-base text-muted-foreground mb-6">
                    {t.agentsPage.whatP2a}<strong>{t.agentsPage.whatP2Strong}</strong>{t.agentsPage.whatP2b}
                </p>
            </section>

            {/* How to Use */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.agentsPage.howTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-6">
                    <strong>{t.agentsPage.howP1Strong}</strong>{t.agentsPage.howP1b}
                </p>

                <div className="relative group mb-6">
                    <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                        <code className="text-code-foreground">{`You: "Add JWT authentication"
AI: 🤖 Applying @security-auditor + @backend-specialist...

You: "Fix the dark mode button"
AI: 🤖 Using @frontend-specialist...

You: "Login returns 500 error"
AI: 🤖 Using @debugger for systematic analysis...`}</code>
                    </pre>
                </div>

                <p className="text-base text-muted-foreground mb-6">
                    {t.agentsPage.howP2a}<strong>{t.agentsPage.howP2Strong}</strong>{t.agentsPage.howP2b}
                </p>

                <div className="relative group mb-6">
                    <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                        <code className="text-code-foreground">{`Use the security-auditor agent to review authentication...`}</code>
                    </pre>
                </div>

                <div className="p-4 rounded-lg border border-blue-200 dark:border-blue-900 bg-blue-50 dark:bg-blue-950/20 mb-6">
                    <p className="text-sm text-blue-900 dark:text-blue-200">
                        <Lightbulb className="w-4 h-4 inline" />
                        <strong className="font-semibold">{t.agentsPage.tipStrong}</strong>{t.agentsPage.tipTextA}<code className="px-1 py-0.5 rounded bg-blue-100 dark:bg-blue-900/40 font-mono text-xs">orchestrator</code>{t.agentsPage.tipTextB}
                    </p>
                </div>
            </section>

            {/* Available Agents */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.agentsPage.availableTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-6">
                    {t.agentsPage.availablePa}{agents.length}{t.agentsPage.availablePb}
                </p>

                <div className="space-y-4">
                    {agents.map((agent) => (
                        <div
                            key={agent.name}
                            className="p-5 rounded-lg border border-border hover:border-border hover:bg-muted transition-all"
                        >
                            <div className="flex items-start justify-between gap-4 mb-2">
                                <code className="text-base font-mono font-semibold text-foreground">
                                    {agent.name}
                                </code>
                            </div>
                            <p className="text-sm text-muted-foreground leading-relaxed">
                                {agent.description}
                            </p>
                        </div>
                    ))}
                </div>
            </section>

            {/* Agent Structure */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.agentsPage.structureTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-6">
                    {t.agentsPage.structureP}
                </p>

                <div className="relative group mb-6">
                    <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                        <code className="text-code-foreground">{`---
name: frontend-specialist
description: Frontend architect expert
tools: Read, Edit, Write, Bash
skills: nextjs-react-expert, tailwind-patterns, frontend-design
---

# Frontend Specialist

You are a senior frontend architect...`}</code>
                    </pre>
                </div>

                <p className="text-base text-muted-foreground">
                    {t.agentsPage.structureNoteA}<code className="px-1.5 py-0.5 rounded bg-muted text-sm font-mono">skills</code>{t.agentsPage.structureNoteB}
                </p>
            </section>

            


            
        </div>
    );
}
