"use client";

import Link from "next/link";
import changelog from "@/services/changelog.json";
import { useI18n } from "@/i18n/provider";

const SECTION_STYLE: Record<string, string> = {
    Added: "text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-900 bg-emerald-50 dark:bg-emerald-950/20",
    Changed: "text-blue-700 dark:text-blue-400 border-blue-200 dark:border-blue-900 bg-blue-50 dark:bg-blue-950/20",
    Fixed: "text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-900 bg-amber-50 dark:bg-amber-950/20",
    Removed: "text-red-700 dark:text-red-400 border-red-200 dark:border-red-900 bg-red-50 dark:bg-red-950/20",
};

export default function ChangelogPage() {
    const { t } = useI18n();
    const c = t.changelogPage;
    const sectionLabel: Record<string, string> = {
        Added: c.added,
        Changed: c.changed,
        Fixed: c.fixed,
        Removed: c.removed,
    };

    return (
        <div className="max-w-3xl">
            {/* Breadcrumb */}
            <nav className="flex items-center gap-2 text-sm text-muted-foreground mb-6">
                <Link href="/docs" className="hover:text-foreground">{c.breadcrumbDocs}</Link>
                <span>/</span>
                <span className="text-foreground">{c.breadcrumbCurrent}</span>
            </nav>

            {/* Page Header */}
            <div className="mb-8 pb-8 border-b border-border">
                <h1 className="text-4xl font-bold tracking-tight text-foreground mb-4">
                    {c.title}
                </h1>
                <p className="text-lg text-muted-foreground">
                    {c.subtitle}
                </p>
            </div>

            {/* Releases */}
            <div className="space-y-12">
                {changelog.map((release) => (
                    <section key={release.version} className="scroll-mt-20" id={`v${release.version}`}>
                        <div className="flex items-baseline gap-3 mb-3">
                            <h2 className="text-2xl font-bold tracking-tight text-foreground">
                                {release.version}
                            </h2>
                            <time className="text-sm font-mono text-muted-foreground">
                                {release.date}
                            </time>
                        </div>

                        {release.summary && (
                            <p className="text-base text-muted-foreground mb-6 border-l-2 border-border pl-4">
                                {release.summary}
                            </p>
                        )}

                        <div className="space-y-5">
                            {Object.entries(release.changes).map(([section, items]) => (
                                <div key={section}>
                                    <span className={`inline-block text-xs font-semibold px-2 py-0.5 rounded border mb-2 ${SECTION_STYLE[section] ?? ""}`}>
                                        {sectionLabel[section] ?? section}
                                    </span>
                                    <ul className="list-disc list-outside pl-5 space-y-1.5 text-sm text-muted-foreground marker:text-muted-foreground">
                                        {(items as string[]).map((item, i) => (
                                            <li key={i} className="pl-1">{item}</li>
                                        ))}
                                    </ul>
                                </div>
                            ))}
                        </div>
                    </section>
                ))}
            </div>

            {/* Footer link */}
            <div className="mt-12 pt-8 border-t border-border">
                <a
                    href="https://github.com/vudovn/ag-kit/releases"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-muted-foreground hover:text-foreground underline underline-offset-4"
                >
                    {c.fullOnGithub} →
                </a>
            </div>
        </div>
    );
}
