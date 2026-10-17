"use client";

import {
  Blocks,
  Bot,
  GitBranch,
  Shield,
  Terminal,
  Workflow,
  type LucideIcon,
} from "lucide-react";
import { useI18n } from "@/i18n/provider";

const icons: LucideIcon[] = [
  Bot,
  Blocks,
  Workflow,
  Terminal,
  Shield,
  GitBranch,
];

export function LandingSponsors() {
  const { t } = useI18n();
  const stack = t.landing.stack;
  const items = stack.items.map((name, i) => ({
    icon: icons[i],
    name,
  }));

  return (
    <section
      id="stack"
      className="mx-auto w-full max-w-[90%] pb-16 sm:max-w-[75%] sm:pb-24"
    >
      <h2 className="mb-8 text-center text-lg text-muted-foreground md:text-xl">
        {stack.title}
      </h2>

      <div className="relative w-full overflow-hidden">
        <div className="landing-marquee flex w-max gap-12">
          {[...items, ...items].map(({ icon: Icon, name }, i) => (
            <div
              key={`${name}-${i}`}
              className="flex items-center gap-2 text-xl font-medium text-foreground/80 md:text-2xl"
            >
              <Icon className="size-7 text-brand" aria-hidden />
              {name}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
