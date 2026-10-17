import type { Metadata } from "next";
import LocalizedDoc from "@/components/docs/localized-doc";
import En from "./content.en.mdx";
import Vi from "./content.vi.mdx";
import Zh from "./content.zh.mdx";
import Ja from "./content.ja.mdx";

export const metadata: Metadata = {
    title: "Example: Project Status | AG Kit",
    description:
        "Learn how to use the /status workflow to view your project and agent status at a glance.",
};

export default function Page() {
    return <LocalizedDoc en={<En />} vi={<Vi />} zh={<Zh />} ja={<Ja />} />;
}
