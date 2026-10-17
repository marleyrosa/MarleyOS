import type { Metadata } from "next";
import LocalizedDoc from "@/components/docs/localized-doc";
import En from "./content.en.mdx";
import Vi from "./content.vi.mdx";
import Zh from "./content.zh.mdx";
import Ja from "./content.ja.mdx";

export const metadata: Metadata = {
    title: "Example: Add a New Feature | AG Kit",
    description:
        "Step-by-step guide on adding new features to an existing application using AG Kit workflows.",
};

export default function Page() {
    return <LocalizedDoc en={<En />} vi={<Vi />} zh={<Zh />} ja={<Ja />} />;
}
