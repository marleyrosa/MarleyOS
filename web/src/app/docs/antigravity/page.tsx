import type { Metadata } from "next";
import LocalizedDoc from "@/components/docs/localized-doc";
import En from "./content.en.mdx";
import Vi from "./content.vi.mdx";

export const metadata: Metadata = {
    title: "Antigravity Runtime Integration | AG Kit",
    description:
        "AG Kit's native Antigravity layer: the runtime contract, PreToolUse safety hook, MCP sync helper, Doctor diagnostics, and plugin bundle.",
};

export default function Page() {
    return <LocalizedDoc en={<En />} vi={<Vi />} />;
}
