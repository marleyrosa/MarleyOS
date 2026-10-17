"use client";

import Image from "next/image";
import Link from "next/link";
import { Separator } from "@/components/ui/separator";
import { useI18n } from "@/i18n/provider";

export function LandingFooter() {
  const { t } = useI18n();
  const f = t.landing.footer;

  return (
    <footer
      id="footer"
      className="container mx-auto px-4 py-16 sm:px-6 sm:py-24 lg:px-8"
    >
      <div className="rounded-2xl border border-border bg-card p-8 md:p-10">
        <div className="grid grid-cols-2 gap-x-10 gap-y-8 md:grid-cols-4 xl:grid-cols-6">
          <div className="col-span-full xl:col-span-2">
            <Link href="/" className="flex items-center gap-2 font-bold">
              <Image
                src="/images/logo.png"
                alt="AG Kit"
                width={36}
                height={36}
                className="size-9 rounded-lg"
              />
              <span className="text-2xl">AG Kit</span>
            </Link>
            <p className="mt-3 max-w-xs text-sm text-muted-foreground">
              {f.blurb}
            </p>
          </div>

          <div className="flex flex-col gap-2">
            <h3 className="text-lg font-bold">{f.product}</h3>
            <Link href="/docs" className="opacity-75 hover:opacity-100">
              {f.documentation}
            </Link>
            <Link href="/docs/agents" className="opacity-75 hover:opacity-100">
              {f.agents}
            </Link>
            <Link href="/docs/skills" className="opacity-75 hover:opacity-100">
              {f.skills}
            </Link>
            <Link
              href="/docs/workflows"
              className="opacity-75 hover:opacity-100"
            >
              {f.workflows}
            </Link>
          </div>

          <div className="flex flex-col gap-2">
            <h3 className="text-lg font-bold">{f.resources}</h3>
            <Link
              href="/docs/installation"
              className="opacity-75 hover:opacity-100"
            >
              {f.installation}
            </Link>
            <Link href="/docs/cli" className="opacity-75 hover:opacity-100">
              {f.cli}
            </Link>
            <Link
              href="/docs/changelog"
              className="opacity-75 hover:opacity-100"
            >
              {f.changelog}
            </Link>
          </div>

          <div className="flex flex-col gap-2">
            <h3 className="text-lg font-bold">{f.community}</h3>
            <a
              href="https://github.com/vudovn/ag-kit"
              target="_blank"
              rel="noopener noreferrer"
              className="opacity-75 hover:opacity-100"
            >
              {f.github}
            </a>
            <a
              href="https://github.com/vudovn/ag-kit/issues"
              target="_blank"
              rel="noopener noreferrer"
              className="opacity-75 hover:opacity-100"
            >
              {f.issues}
            </a>
            <a
              href="https://github.com/vudovn/ag-kit/discussions"
              target="_blank"
              rel="noopener noreferrer"
              className="opacity-75 hover:opacity-100"
            >
              {f.discussions}
            </a>
          </div>

          <div className="flex flex-col gap-2">
            <h3 className="text-lg font-bold">{f.legal}</h3>
            <a
              href="https://github.com/vudovn/ag-kit/blob/main/LICENSE"
              target="_blank"
              rel="noopener noreferrer"
              className="opacity-75 hover:opacity-100"
            >
              {f.license}
            </a>
            <a
              href="https://github.com/vudovn/ag-kit/blob/main/SECURITY.md"
              target="_blank"
              rel="noopener noreferrer"
              className="opacity-75 hover:opacity-100"
            >
              {f.security}
            </a>
          </div>
        </div>

        <Separator className="my-8" />

        <p className="text-sm text-muted-foreground">
          &copy; {new Date().getFullYear()} AG Kit by{" "}
          <a
            href="https://github.com/vudovn"
            target="_blank"
            rel="noopener noreferrer"
            className="text-foreground transition-colors hover:text-brand"
          >
            @vudovn
          </a>
          . {f.credit}{" "}
          <a
            href="https://github.com/nobruf/shadcn-landing-page"
            target="_blank"
            rel="noopener noreferrer"
            className="text-foreground transition-colors hover:text-brand"
          >
            shadcn-landing-page
          </a>
          .
        </p>
      </div>
    </footer>
  );
}
