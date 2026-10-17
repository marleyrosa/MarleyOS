// Single source of truth for docs navigation.
// Consumed by the sidebar, mobile menu, search dialog, and prev/next pager.
// `labelKey` points into the i18n `search` dictionary when a translation
// exists; `label` is the fallback (guide titles are English-only for now).

export interface DocsNavItem {
    href: string;
    label: string;
    labelKey?: string;
    keywords?: string;
}

export interface DocsNavSection {
    title: string;
    titleKey?: string;
    items: DocsNavItem[];
}

export const docsNav: DocsNavSection[] = [
    {
        title: "Getting Started",
        titleKey: "groupGettingStarted",
        items: [
            { href: "/docs", label: "Introduction", labelKey: "introduction", keywords: "getting started overview what is" },
            { href: "/docs/installation", label: "Installation", labelKey: "installation", keywords: "install setup init npm npx global cli" },
        ],
    },
    {
        title: "Core Concepts",
        titleKey: "groupCoreConcepts",
        items: [
            { href: "/docs/agents", label: "Agents", labelKey: "agents", keywords: "specialist personas orchestrator planner security backend frontend" },
            { href: "/docs/skills", label: "Skills", labelKey: "skills", keywords: "knowledge modules react nextjs tailwind patterns testing" },
            { href: "/docs/workflows", label: "Workflows", labelKey: "workflows", keywords: "slash commands brainstorm create debug deploy enhance" },
            { href: "/docs/updates", label: "Managed Updates & Rollback", keywords: "update rollback backup merge replace manifest lock sha-256 conflicts safe" },
            { href: "/docs/antigravity", label: "Antigravity Runtime", keywords: "antigravity hooks pretooluse mcp sync doctor plugin contract safety" },
        ],
    },
    {
        title: "Guide",
        items: [
            { href: "/docs/guide/examples/brainstorm", label: "Structured Brainstorming", keywords: "brainstorm ideas explore" },
            { href: "/docs/guide/examples/plan", label: "Project Planning", keywords: "plan phases tasks" },
            { href: "/docs/guide/examples/create", label: "Create New Application", keywords: "create scaffold new app" },
            { href: "/docs/guide/examples/new-feature", label: "Add a New Feature", keywords: "feature existing project enhance" },
            { href: "/docs/guide/examples/debugging", label: "Systematic Debugging", keywords: "debug fix error root cause" },
            { href: "/docs/guide/examples/test", label: "Test Generation", keywords: "test unit integration coverage" },
            { href: "/docs/guide/examples/preview", label: "Preview Management", keywords: "preview dev server start stop" },
            { href: "/docs/guide/examples/status", label: "Project Status", keywords: "status memory context recall" },
            { href: "/docs/guide/examples/orchestration", label: "Multi-Agent Orchestration", keywords: "orchestrate coordinate parallel agents tasks" },
            { href: "/docs/guide/examples/deployment", label: "Production Deployment", keywords: "deploy production release checks" },
        ],
    },
    {
        title: "CLI Reference",
        titleKey: "groupReference",
        items: [
            { href: "/docs/cli", label: "Commands & Options", labelKey: "commandsOptions", keywords: "command line interface init update rollback status strategy dry-run options" },
            { href: "/docs/changelog", label: "Changelog", keywords: "changelog releases versions history" },
        ],
    },
];

export const docsNavFlat: DocsNavItem[] = docsNav.flatMap((section) => section.items);
