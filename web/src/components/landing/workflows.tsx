"use client";

import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { buttonVariants } from "@/components/ui/button";
import { useI18n } from "@/i18n/provider";
import { cn } from "@/lib/utils";

const HREFS = [
  "/docs/guide/examples/brainstorm",
  "/docs/guide/examples/plan",
  "/docs/guide/examples/create",
  "/docs/guide/examples/debugging",
  "/docs/guide/examples/orchestration",
  "/docs/guide/examples/deployment",
] as const;

export function LandingWorkflows() {
  const { t } = useI18n();
  const copy = t.landing.workflows;
  const workflows = copy.items.map((item, i) => ({
    ...item,
    href: HREFS[i],
  }));

  return (
    <section
      id="workflows"
      className="container mx-auto px-4 py-20 sm:px-6 sm:py-28 lg:px-8"
    >
      <p className="mb-2 text-center text-lg tracking-wider text-brand">
        {copy.eyebrow}
      </p>
      <h2 className="mb-4 text-center text-3xl font-bold tracking-tight md:text-4xl">
        {copy.title}
      </h2>
      <p className="mx-auto mb-10 max-w-2xl text-center text-lg text-muted-foreground md:text-xl">
        {copy.subtitle}
      </p>

      <div className="mx-auto grid w-full max-w-4xl gap-4 sm:grid-cols-2">
        {workflows.map(({ title, description, href, highlight }) => (
          <Link key={title} href={href} className="group relative block">
            <Card className="h-full bg-muted/60 transition-colors group-hover:border-brand/40 dark:bg-card">
              <CardHeader>
                <CardTitle className="font-mono text-brand">{title}</CardTitle>
                <CardDescription>{description}</CardDescription>
              </CardHeader>
              {highlight ? (
                <Badge
                  variant="secondary"
                  className="absolute -top-2 -right-2"
                >
                  {copy.core}
                </Badge>
              ) : null}
            </Card>
          </Link>
        ))}
      </div>

      <div className="mt-10 flex justify-center">
        <Link
          href="/docs/workflows"
          className={cn(buttonVariants({ variant: "outline", size: "lg" }))}
        >
          {copy.browseAll}
        </Link>
      </div>
    </section>
  );
}
