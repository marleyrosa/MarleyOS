import type { Metadata } from "next";
import LocalizedDoc from "@/components/docs/localized-doc";
import En from "./content.en.mdx";
import Vi from "./content.vi.mdx";

export const metadata: Metadata = {
    title: "Managed Updates & Rollback | AG Kit",
    description:
        "How AG Kit's managed tree, SHA-256 manifest lock, merge-aware updates, backups, and rollback keep your local changes safe.",
};

export default function Page() {
    return <LocalizedDoc en={<En />} vi={<Vi />} />;
}
