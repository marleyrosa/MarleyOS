import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "AG Kit - AI Agent Capability Expansion Toolkit",
    short_name: "AG Kit",
    description:
      "A comprehensive collection of 47 skills, 20 specialist agents, rules, and production-ready workflows for modern AI coding assistants.",
    start_url: "/",
    display: "standalone",
    background_color: "#09090b",
    theme_color: "#2dd4bf",
    icons: [
      {
        src: "/favicon.ico",
        sizes: "any",
        type: "image/x-icon",
      },
      {
        src: "/images/logo.svg",
        sizes: "any",
        type: "image/svg+xml",
      },
      {
        src: "/images/logo.png",
        sizes: "1024x1024",
        type: "image/png",
      },
    ],
  };
}
