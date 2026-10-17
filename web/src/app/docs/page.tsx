"use client";

import Link from "next/link";
import agents from '@/services/agents.json';
import skills from '@/services/skills.json';
import workflows from '@/services/workflows.json';
import { useI18n } from "@/i18n/provider";

export default function DocsPage() {
    const { t } = useI18n();
    return (
        <div className="max-w-3xl">
            {/* Page Header */}
            <div className="mb-8 pb-8 border-b border-border">
                <h1 className="text-4xl font-bold tracking-tight text-foreground mb-4">
                    {t.docsHome.title}
                </h1>
                <p className="text-lg text-muted-foreground">
                    {t.docsHome.welcomePre}<span className="brand-mark">
                        AG Kit
                    </span>{t.docsHome.welcomePost}
                </p>
            </div>

            {/* What is AG Kit */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.docsHome.whatIsPre}<span className="brand-mark">
                        AG Kit
                    </span>{t.docsHome.whatIsPost}
                </h2>
                <p className="text-base text-muted-foreground mb-4">
                    <span className="brand-mark">
                        AG Kit
                    </span>{t.docsHome.whatIsP1}
                </p>
                <p className="text-base text-muted-foreground mb-4">
                    {t.docsHome.whatIsP2a}{skills.length}{t.docsHome.whatIsP2b}{agents.length}{t.docsHome.whatIsP2c}{workflows.length}{t.docsHome.whatIsP2d}
                </p>
            </section>

            {/* What's Included */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.docsHome.includedTitle}
                </h2>
                <div className="grid gap-4 sm:grid-cols-3 mb-6">
                    <div className="p-6 rounded-lg border border-border bg-muted">
                        <div className="text-3xl font-bold text-foreground mb-2">{agents.length}+</div>
                        <div className="text-sm font-medium text-muted-foreground">{t.docsHome.specialistAgents}</div>
                        <p className="text-xs text-muted-foreground mt-2">
                            {t.docsHome.specialistAgentsDesc}
                        </p>
                    </div>
                    <div className="p-6 rounded-lg border border-border bg-muted">
                        <div className="text-3xl font-bold text-foreground mb-2">{skills.length}+</div>
                        <div className="text-sm font-medium text-muted-foreground">{t.docsHome.domainSkills}</div>
                        <p className="text-xs text-muted-foreground mt-2">
                            {t.docsHome.domainSkillsDesc}
                        </p>
                    </div>
                    <div className="p-6 rounded-lg border border-border bg-muted">
                        <div className="text-3xl font-bold text-foreground mb-2">{workflows.length}+</div>
                        <div className="text-sm font-medium text-muted-foreground">{t.docsHome.workflowsLabel}</div>
                        <p className="text-xs text-muted-foreground mt-2">
                            {t.docsHome.workflowsDesc}
                        </p>
                    </div>
                </div>
            </section>

            {/* How to Use the Docs */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.docsHome.howToTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-4">
                    {t.docsHome.howToP}
                </p>
                <div className="space-y-4 mb-6">
                    <div className="p-4 rounded-lg border border-border">
                        <Link href="/docs/installation" className="font-semibold text-foreground hover:underline">
                            {t.docsHome.gettingStarted}
                        </Link>
                        <p className="text-sm text-muted-foreground mt-1">
                            {t.docsHome.gettingStartedDesc}
                        </p>
                    </div>
                    <div className="p-4 rounded-lg border border-border">
                        <Link href="/docs/agents" className="font-semibold text-foreground hover:underline">
                            {t.docsHome.coreConcepts}
                        </Link>
                        <p className="text-sm text-muted-foreground mt-1">
                            {t.docsHome.coreConceptsDesc}
                        </p>
                    </div>
                    <div className="p-4 rounded-lg border border-border">
                        <Link href="/docs/cli" className="font-semibold text-foreground hover:underline">
                            {t.docsHome.cliRef}
                        </Link>
                        <p className="text-sm text-muted-foreground mt-1">
                            {t.docsHome.cliRefDesc}
                        </p>
                    </div>
                </div>
                <p className="text-sm text-muted-foreground">
                    {t.docsHome.sidebarHintPre}<kbd className="px-2 py-1 text-xs font-mono rounded bg-muted border border-border">Ctrl+K</kbd>{t.docsHome.sidebarHintPost}
                </p>
            </section>

            


            
        </div>
    );
}
