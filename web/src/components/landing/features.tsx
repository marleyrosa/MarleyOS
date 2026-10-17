"use client";

import {
  Bot,
  FolderKanban,
  Puzzle,
  RefreshCw,
  Terminal,
  Workflow,
  type LucideIcon,
} from "lucide-react";
import { useI18n } from "@/i18n/provider";

const icons: LucideIcon[] = [
  Bot,
  Puzzle,
  Workflow,
  Terminal,
  RefreshCw,
  FolderKanban,
];

export function LandingFeatures() {
  const { t } = useI18n();
  const copy = t.landing.features;
  const items = copy.items.map((item, i) => ({
    ...item,
    icon: icons[i],
  }));

  return (
    <section
      id="features"
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

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {items.map(({ icon: Icon, title, description }) => (
          <article
            key={title}
            className="flex h-full flex-col items-center rounded-2xl border border-border bg-card p-6 text-center shadow-xs"
          >
            <div className="mb-5 flex size-14 items-center justify-center rounded-full bg-brand/15 ring-8 ring-brand/10">
              <Icon className="size-6 text-brand" aria-hidden />
            </div>
            <h3 className="mb-2 text-lg font-semibold text-foreground">
              {title}
            </h3>
            <p className="text-sm leading-relaxed text-muted-foreground">
              {description}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
