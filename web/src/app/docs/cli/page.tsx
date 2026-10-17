"use client";

import Link from "next/link";
import { useI18n } from "@/i18n/provider";

export default function CLIPage() {
    const { t } = useI18n();
    return (
        <div className="max-w-3xl">
            {/* Breadcrumb */}
            <nav className="flex items-center gap-2 text-sm text-muted-foreground mb-6">
                <Link href="/docs" className="hover:text-foreground">{t.cliPage.breadcrumbDocs}</Link>
                <span>/</span>
                <span className="text-foreground">{t.cliPage.breadcrumbCurrent}</span>
            </nav>

            {/* Page Header */}
            <div className="mb-8 pb-8 border-b border-border">
                <h1 className="text-4xl font-bold tracking-tight text-foreground mb-4">
                    {t.cliPage.title}
                </h1>
                <p className="text-lg text-muted-foreground">
                    {t.cliPage.subtitle}
                </p>
            </div>

            {/* Overview */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.cliPage.overviewTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-6">
                    {t.cliPage.overviewPa}<code className="px-1.5 py-0.5 rounded bg-muted text-sm font-mono">ag-kit</code>{t.cliPage.overviewPb}
                </p>
            </section>

            {/* Commands */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.cliPage.commandsTitle}
                </h2>

                <div className="space-y-8">
                    {/* init */}
                    <div>
                        <h3 className="text-xl font-semibold text-foreground mb-3">
                            <code className="font-mono">ag-kit init</code>
                        </h3>
                        <p className="text-base text-muted-foreground mb-4">
                            {t.cliPage.initDescA}<code className="px-1.5 py-0.5 rounded bg-muted text-sm font-mono">.agents</code>{t.cliPage.initDescB}
                        </p>

                        <div className="relative group mb-4">
                            <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                                <code className="text-code-foreground">ag-kit init</code>
                            </pre>
                        </div>

                        <div className="p-4 rounded-lg border border-border bg-muted/50">
                            <div className="text-sm font-semibold text-foreground mb-2">{t.cliPage.behaviorTitle}</div>
                            <ul className="text-sm text-muted-foreground space-y-1">
                                <li>• {t.cliPage.initBehavior1a}<code className="px-1 py-0.5 rounded bg-border font-mono text-xs">.agents/</code>{t.cliPage.initBehavior1b}</li>
                                <li>• {t.cliPage.initBehavior2}</li>
                                <li>• {t.cliPage.initBehavior3a}<code className="px-1 py-0.5 rounded bg-border font-mono text-xs">.agents/</code>{t.cliPage.initBehavior3b}<code className="px-1 py-0.5 rounded bg-border font-mono text-xs">--force</code>{t.cliPage.initBehavior3c}</li>
                            </ul>
                        </div>
                    </div>

                    {/* update */}
                    <div>
                        <h3 className="text-xl font-semibold text-foreground mb-3">
                            <code className="font-mono">ag-kit update</code>
                        </h3>
                        <p className="text-base text-muted-foreground mb-4">
                            {t.cliPage.updateDesc}
                        </p>

                        <div className="relative group mb-4">
                            <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                                <code className="text-code-foreground">ag-kit update</code>
                            </pre>
                        </div>

                        <div className="p-4 rounded-lg border border-amber-200 dark:border-amber-900 bg-amber-50 dark:bg-amber-950/20">
                            <p className="text-sm text-amber-900 dark:text-amber-200">
                                <strong className="font-semibold">{t.cliPage.updateWarningStrong}</strong>{t.cliPage.updateWarningA}<code className="px-1 py-0.5 rounded bg-amber-100 dark:bg-amber-900/40 font-mono text-xs">.agents/</code>{t.cliPage.updateWarningB}
                            </p>
                        </div>
                    </div>

                    {/* rollback */}
                    <div>
                        <h3 className="text-xl font-semibold text-foreground mb-3">
                            <code className="font-mono">ag-kit rollback</code>
                        </h3>
                        <p className="text-base text-muted-foreground mb-4">
                            {t.cliPage.rollbackDesc}
                        </p>

                        <div className="relative group mb-4">
                            <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                                <code className="text-code-foreground">ag-kit rollback</code>
                            </pre>
                        </div>

                        <div className="p-4 rounded-lg border border-border bg-muted/50">
                            <div className="text-sm font-semibold text-foreground mb-2">{t.cliPage.behaviorTitle}</div>
                            <ul className="text-sm text-muted-foreground space-y-1">
                                <li>• {t.cliPage.rollbackBehavior1}</li>
                                <li>• {t.cliPage.rollbackBehavior2}</li>
                                <li>• {t.cliPage.rollbackBehavior3}</li>
                            </ul>
                        </div>
                    </div>

                    {/* status */}
                    <div>
                        <h3 className="text-xl font-semibold text-foreground mb-3">
                            <code className="font-mono">ag-kit status</code>
                        </h3>
                        <p className="text-base text-muted-foreground mb-4">
                            {t.cliPage.statusDesc}
                        </p>

                        <div className="relative group mb-4">
                            <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                                <code className="text-code-foreground">ag-kit status</code>
                            </pre>
                        </div>

                        <div className="p-4 rounded-lg border border-border bg-muted/50">
                            <div className="text-sm font-semibold text-foreground mb-2">{t.cliPage.outputIncludesTitle}</div>
                            <ul className="text-sm text-muted-foreground space-y-1">
                                <li>• {t.cliPage.statusOut1}</li>
                                <li>• {t.cliPage.statusOut2}</li>
                                <li>• {t.cliPage.statusOut3}</li>
                                <li>• {t.cliPage.statusOut4a}<code className="px-1 py-0.5 rounded bg-muted font-mono text-xs">.agents</code>{t.cliPage.statusOut4b}</li>
                                <li>• {t.cliPage.statusOut5}</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            {/* Options */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.cliPage.optionsTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-6">
                    {t.cliPage.optionsP}
                </p>

                <div className="overflow-x-auto">
                    <table className="w-full text-sm border border-border">
                        <thead className="bg-muted/50">
                            <tr>
                                <th className="text-left py-3 px-4 font-semibold text-foreground border-b border-border">{t.cliPage.tableOption}</th>
                                <th className="text-left py-3 px-4 font-semibold text-foreground border-b border-border">{t.cliPage.tableDescription}</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border">
                            <tr>
                                <td className="py-3 px-4">
                                    <code className="font-mono text-foreground">-f, --force</code>
                                </td>
                                <td className="py-3 px-4 text-muted-foreground">
                                    {t.cliPage.optForceA}<code className="px-1 py-0.5 rounded bg-muted font-mono text-xs">.agents</code>{t.cliPage.optForceB}<code className="px-1 py-0.5 rounded bg-muted font-mono text-xs">update</code>{t.cliPage.optForceC}
                                </td>
                            </tr>
                            <tr>
                                <td className="py-3 px-4">
                                    <code className="font-mono text-foreground">-p, --path &lt;dir&gt;</code>
                                </td>
                                <td className="py-3 px-4 text-muted-foreground">
                                    {t.cliPage.optPathDesc}
                                </td>
                            </tr>
                            <tr>
                                <td className="py-3 px-4">
                                    <code className="font-mono text-foreground">-b, --branch &lt;name&gt;</code>
                                </td>
                                <td className="py-3 px-4 text-muted-foreground">
                                    {t.cliPage.optBranchDesc}
                                </td>
                            </tr>
                            <tr>
                                <td className="py-3 px-4">
                                    <code className="font-mono text-foreground">-q, --quiet</code>
                                </td>
                                <td className="py-3 px-4 text-muted-foreground">
                                    {t.cliPage.optQuietDesc}
                                </td>
                            </tr>
                            <tr>
                                <td className="py-3 px-4">
                                    <code className="font-mono text-foreground">--dry-run</code>
                                </td>
                                <td className="py-3 px-4 text-muted-foreground">
                                    {t.cliPage.optDryRunA}<code className="px-1 py-0.5 rounded bg-muted font-mono text-xs">init</code>{t.cliPage.optDryRunB}<code className="px-1 py-0.5 rounded bg-muted font-mono text-xs">update</code>{t.cliPage.optDryRunC}
                                </td>
                            </tr>
                            <tr>
                                <td className="py-3 px-4">
                                    <code className="font-mono text-foreground">--strategy &lt;merge|replace&gt;</code>
                                </td>
                                <td className="py-3 px-4 text-muted-foreground">
                                    {t.cliPage.optStrategyDesc}
                                </td>
                            </tr>
                            <tr>
                                <td className="py-3 px-4">
                                    <code className="font-mono text-foreground">--no-backup</code>
                                </td>
                                <td className="py-3 px-4 text-muted-foreground">
                                    {t.cliPage.optNoBackupDesc}
                                </td>
                            </tr>
                            <tr>
                                <td className="py-3 px-4">
                                    <code className="font-mono text-foreground">--conflict-report &lt;file&gt;</code>
                                </td>
                                <td className="py-3 px-4 text-muted-foreground">
                                    {t.cliPage.optConflictReportDesc}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            {/* Examples */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.cliPage.examplesTitle}
                </h2>

                <div className="space-y-6">
                    <div>
                        <h3 className="text-base font-semibold text-foreground mb-2">
                            {t.cliPage.exForceReinstall}
                        </h3>
                        <div className="relative group">
                            <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                                <code className="text-code-foreground">ag-kit init --force</code>
                            </pre>
                        </div>
                    </div>

                    <div>
                        <h3 className="text-base font-semibold text-foreground mb-2">
                            {t.cliPage.exInstallDir}
                        </h3>
                        <div className="relative group">
                            <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                                <code className="text-code-foreground">ag-kit init --path ./my-project</code>
                            </pre>
                        </div>
                    </div>

                    <div>
                        <h3 className="text-base font-semibold text-foreground mb-2">
                            {t.cliPage.exDevBranch}
                        </h3>
                        <div className="relative group">
                            <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                                <code className="text-code-foreground">ag-kit init --branch dev</code>
                            </pre>
                        </div>
                    </div>

                    <div>
                        <h3 className="text-base font-semibold text-foreground mb-2">
                            {t.cliPage.exSilentCI}
                        </h3>
                        <div className="relative group">
                            <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                                <code className="text-code-foreground">ag-kit init --quiet --force</code>
                            </pre>
                        </div>
                    </div>

                    <div>
                        <h3 className="text-base font-semibold text-foreground mb-2">
                            {t.cliPage.exPreviewUpdate}
                        </h3>
                        <div className="relative group">
                            <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                                <code className="text-code-foreground">ag-kit update --dry-run</code>
                            </pre>
                        </div>
                    </div>

                    <div>
                        <h3 className="text-base font-semibold text-foreground mb-2">
                            {t.cliPage.exReplace}
                        </h3>
                        <div className="relative group">
                            <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                                <code className="text-code-foreground">ag-kit update --strategy replace</code>
                            </pre>
                        </div>
                    </div>

                    <div>
                        <h3 className="text-base font-semibold text-foreground mb-2">
                            {t.cliPage.exRollbackLatest}
                        </h3>
                        <div className="relative group">
                            <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                                <code className="text-code-foreground">ag-kit rollback</code>
                            </pre>
                        </div>
                    </div>
                </div>
            </section>

            


            
        </div>
    );
}
