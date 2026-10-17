import type { MetadataRoute } from "next";

const BASE = "https://ag-kit.unikorn.vn";

const GUIDE_EXAMPLES = [
    "brainstorm",
    "plan",
    "create",
    "new-feature",
    "debugging",
    "test",
    "preview",
    "status",
    "orchestration",
    "deployment",
];

export default function sitemap(): MetadataRoute.Sitemap {
    const routes = [
        "",
        "/docs",
        "/docs/installation",
        "/docs/agents",
        "/docs/skills",
        "/docs/workflows",
        "/docs/updates",
        "/docs/antigravity",
        "/docs/cli",
        "/docs/changelog",
        ...GUIDE_EXAMPLES.map((slug) => `/docs/guide/examples/${slug}`),
    ];
    return routes.map((route) => ({
        url: `${BASE}${route}`,
        changeFrequency: route === "/docs/changelog" ? "weekly" : "monthly",
        priority: route === "" ? 1 : route === "/docs" ? 0.9 : 0.7,
    }));
}
