"use client";

import { Lightbulb } from "lucide-react";
import Link from "next/link";
import workflowsData from "@/services/workflows.json";
import { useI18n } from "@/i18n/provider";

export default function WorkflowsPage() {
    const { t } = useI18n();
    // Add default usage examples if not in JSON (since ARCHITECTURE.md didn't have usage)
    const workflows = workflowsData.map(wf => ({
        ...wf,
        usage: wf.command + " [args]", // Simple default usage
    }));

    return (
        <div className="max-w-3xl">
            {/* Breadcrumb */}
            <nav className="flex items-center gap-2 text-sm text-muted-foreground mb-6">
                <Link href="/docs" className="hover:text-foreground">{t.workflowsPage.breadcrumbDocs}</Link>
                <span>/</span>
                <span className="text-foreground">{t.workflowsPage.breadcrumbCurrent}</span>
            </nav>

            {/* Page Header */}
            <div className="mb-8 pb-8 border-b border-border">
                <h1 className="text-4xl font-bold tracking-tight text-foreground mb-4">
                    {t.workflowsPage.title}
                </h1>
                <p className="text-lg text-muted-foreground">
                    {t.workflowsPage.subtitle}
                </p>
            </div>

            {/* What are Workflows */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.workflowsPage.whatTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-4">
                    {t.workflowsPage.whatP1}
                </p>
                <p className="text-base text-muted-foreground mb-6">
                    {t.workflowsPage.whatP2}
                </p>
            </section>

            {/* How to Use */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.workflowsPage.howTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-6">
                    {t.workflowsPage.howP}
                </p>

                <div className="relative group mb-6">
                    <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                        <code className="text-code-foreground">{`/brainstorm authentication system
/create landing page with hero section
/debug why login fails`}</code>
                    </pre>
                </div>

                <div className="bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-4">
                    <p className="text-sm text-blue-900 dark:text-blue-100 mb-0">
                        <Lightbulb className="w-4 h-4 inline" />
                        <strong className="font-semibold">{t.workflowsPage.tipStrong}</strong>{t.workflowsPage.tipTextA}<code className="px-1 py-0.5 rounded bg-blue-100 dark:bg-blue-900/40 font-mono text-xs">{'// turbo'}</code>{t.workflowsPage.tipTextB}
                    </p>
                </div>
            </section>

            {/* Available Workflows */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.workflowsPage.availableTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-6">
                    {workflows.length}{t.workflowsPage.availablePb}
                </p>

                <div className="space-y-6">
                    {workflows.map((workflow) => (
                        <div
                            key={workflow.command}
                            className="p-5 rounded-lg border border-border"
                        >
                            <div className="flex items-start justify-between gap-4 mb-3">
                                <code className="text-lg font-mono font-semibold text-foreground">
                                    {workflow.command}
                                </code>
                            </div>
                            <p className="text-sm text-muted-foreground mb-3 leading-relaxed">
                                {workflow.description}
                            </p>
                            <div className="pt-3 border-t border-border">
                                <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                                    {t.workflowsPage.exampleUsage}
                                </div>
                                <code className="text-sm font-mono text-muted-foreground bg-muted px-2 py-1 rounded">
                                    {workflow.usage}
                                </code>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Creating Custom Workflows */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.workflowsPage.customTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-6">
                    {t.workflowsPage.customPa}<code className="px-1.5 py-0.5 rounded bg-muted text-sm font-mono">.agents/workflows/</code>{t.workflowsPage.customPb}
                </p>

                <div className="relative group mb-6">
                    <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                        <code className="text-code-foreground">{`---
description: Deploy application to staging
---

# Deployment Workflow

1. Run tests
2. Build production bundle
3. Deploy to staging server
4. Verify deployment`}</code>
                    </pre>
                </div>

                <p className="text-base text-muted-foreground">
                    {t.workflowsPage.customNoteA}<code className="px-1.5 py-0.5 rounded bg-muted text-sm font-mono">.agents/workflows/deploy-staging.md</code>{t.workflowsPage.customNoteB}<code className="px-1.5 py-0.5 rounded bg-muted text-sm font-mono">/deploy-staging</code>{t.workflowsPage.customNoteC}
                </p>
            </section>

            


            
        </div>
    );
}
