"use client";

import {
  GitMerge,
  LineChart,
  ShieldCheck,
  Sparkles,
  type LucideIcon,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useI18n } from "@/i18n/provider";

const icons: LucideIcon[] = [Sparkles, ShieldCheck, GitMerge, LineChart];

export function LandingBenefits() {
  const { t } = useI18n();
  const copy = t.landing.benefits;
  const items = copy.items.map((item, i) => ({
    ...item,
    icon: icons[i],
  }));

  return (
    <section
      id="benefits"
      className="container mx-auto px-4 py-20 sm:px-6 sm:py-28 lg:px-8"
    >
      <div className="grid place-items-center gap-12 lg:grid-cols-2 lg:gap-20">
        <div>
          <p className="mb-2 text-lg tracking-wider text-brand">
            {copy.eyebrow}
          </p>
          <h2 className="mb-4 text-3xl font-bold tracking-tight md:text-4xl">
            {copy.title}
          </h2>
          <p className="text-lg text-muted-foreground md:text-xl">
            {copy.subtitle}
          </p>
        </div>

        <div className="grid w-full gap-4 sm:grid-cols-2">
          {items.map(({ icon: Icon, title, description }, index) => (
            <Card
              key={title}
              className="group/number bg-muted/50 transition-colors hover:bg-background dark:bg-card"
            >
              <CardHeader>
                <div className="flex justify-between">
                  <Icon className="mb-4 size-8 text-brand" />
                  <span className="text-5xl font-medium text-muted-foreground/15 transition-colors group-hover/number:text-muted-foreground/30">
                    0{index + 1}
                  </span>
                </div>
                <CardTitle>{title}</CardTitle>
              </CardHeader>
              <CardContent className="text-muted-foreground">
                {description}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
