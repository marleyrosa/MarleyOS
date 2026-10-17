"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { GithubStarButton } from "@/components/github-star-button";
import { buttonVariants } from "@/components/ui/button";
import { useI18n } from "@/i18n/provider";
import { cn } from "@/lib/utils";

export function LandingHero() {
  const { t } = useI18n();
  const hero = t.landing.hero;

  return (
    <section className="container mx-auto w-full px-4 sm:px-6 lg:px-8">
      <div className="mx-auto grid w-full min-w-0 [grid-template-columns:minmax(0,1fr)] place-items-center gap-8 py-16 md:py-28 lg:max-w-screen-xl">
        <div className="space-y-8 text-center">
          <h1 className="mx-auto max-w-screen-md text-4xl font-bold tracking-tight md:text-6xl">
            {hero.title}{" "}
            <span className="text-brand">
              AG Kit
            </span>
          </h1>

          <p className="mx-auto max-w-screen-sm text-lg text-muted-foreground md:text-xl">
            {hero.subtitle}
          </p>

          <div className="flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Link
              href="/orbital-lab"
              className="inline-flex items-center justify-center gap-2 w-full sm:w-auto px-6 py-3 rounded-lg font-mono font-bold text-sm bg-gradient-to-r from-cyan-600 to-emerald-600 text-white hover:from-cyan-500 hover:to-emerald-500 shadow-[0_0_20px_rgba(6,182,212,0.4)] border border-cyan-400/50 transition-all"
            >
              <span className="w-2 h-2 rounded-full bg-white animate-pulse" />
              LAUNCH ORBITAL PAPER LAB
              <ArrowRight className="size-4" />
            </Link>
            <Link
              href="/docs/installation"
              className={cn(
                buttonVariants({ variant: "outline", size: "lg" }),
                "group/arrow w-full font-semibold sm:w-auto",
              )}
            >
              {hero.getStarted}
            </Link>
            <GithubStarButton
              className="w-full sm:w-auto"
              variant="secondary"
              size="lg"
              label={hero.github}
            />
          </div>
        </div>

        <div className="relative mt-10 w-full min-w-0 max-w-4xl">
          <div className="absolute top-4 left-1/2 h-40 w-[90%] -translate-x-1/2 rounded-full bg-brand/30 blur-3xl lg:-top-6 lg:h-72" />
          <div className="relative overflow-hidden rounded-xl border border-border border-t-brand/40 bg-code shadow-2xl">
            <div className="flex items-center gap-2 border-b border-code-border bg-code-title px-4 py-3">
              <span className="size-3 rounded-full bg-red-500/90" />
              <span className="size-3 rounded-full bg-amber-500/90" />
              <span className="size-3 rounded-full bg-emerald-500/90" />
              <span className="ml-2 font-mono text-xs text-muted-foreground">
                terminal
              </span>
            </div>
            <pre className="overflow-x-auto p-5 font-mono text-sm leading-relaxed text-code-foreground md:p-6 md:text-[15px]">
              <code>
                <span className="text-brand">$</span> npx @vudovn/ag-kit init
                {"\n"}
                <span className="text-muted-foreground">
                  ✓ Downloaded toolkit
                  {"\n"}✓ Installed .agents (skills, agents, workflows)
                  {"\n"}✓ Wrote managed-file manifest
                </span>
                {"\n\n"}
                <span className="text-brand">$</span> ag-kit update
                {"\n"}
                <span className="text-muted-foreground">
                  Strategy: merge · Backup created
                  {"\n"}Updated 12 files · Preserved 3 local · 0 conflicts
                </span>
                {"\n\n"}
                <span className="text-brand">▸</span> /brainstorm auth options
                {"\n"}
                <span className="text-muted-foreground">
                  Exploring 3 approaches before you write code...
                </span>
              </code>
            </pre>
            <div className="pointer-events-none absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-background/80 to-transparent" />
          </div>
        </div>
      </div>
    </section>
  );
}
