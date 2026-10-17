import type { Metadata } from "next";
import LocalizedDoc from "@/components/docs/localized-doc";
import En from "./content.en.mdx";
import Vi from "./content.vi.mdx";
import Zh from "./content.zh.mdx";
import Ja from "./content.ja.mdx";

export const metadata: Metadata = {
    title: "Example: Production Deployment | AG Kit",
    description:
        "Learn how to strictly and safely deploy applications using the /deploy workflow.",
};

export default function Page() {
    return <LocalizedDoc en={<En />} vi={<Vi />} zh={<Zh />} ja={<Ja />} />;
}
