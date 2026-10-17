"use client";

import { useEffect, useState } from "react";
import { GithubStarButton } from "@/components/github-star-button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { buttonVariants } from "@/components/ui/button";
import { useI18n } from "@/i18n/provider";
import {
  fetchGithubContributors,
  type GithubContributor,
  GITHUB_REPO_URL,
} from "@/lib/github";
import { cn } from "@/lib/utils";

export function LandingContribute() {
  const { t } = useI18n();
  const copy = t.landing.contribute;
  const [contributors, setContributors] = useState<GithubContributor[]>([]);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetchGithubContributors().then((list) => {
      if (cancelled) return;
      setContributors(list);
      setLoaded(true);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <section
      id="contribute"
      className="container mx-auto px-4 py-20 sm:px-6 sm:py-28 lg:px-8"
    >
      <p className="mb-2 text-center text-lg tracking-wider text-brand">
        {copy.eyebrow}
      </p>
      <h2 className="mb-4 text-center text-3xl font-bold tracking-tight md:text-4xl">
        {copy.title}
      </h2>
      <p className="mx-auto mb-10 max-w-2xl text-center text-lg text-muted-foreground">
        {copy.subtitle}
      </p>

      <div className="mb-12 flex flex-col items-center justify-center gap-3 sm:flex-row">
        <GithubStarButton
          variant="default"
          size="lg"
          label={copy.starLabel}
        />
        <a
          href={`${GITHUB_REPO_URL}/blob/main/CONTRIBUTING.md`}
          target="_blank"
          rel="noopener noreferrer"
          className={cn(buttonVariants({ size: "lg", variant: "outline" }))}
        >
          {copy.guide}
        </a>
      </div>

      {!loaded ? (
        <p className="text-center text-sm text-muted-foreground">
          {copy.loading}
        </p>
      ) : contributors.length === 0 ? (
        <div className="flex flex-col items-center gap-4 text-center">
          <p className="text-sm text-muted-foreground">{copy.empty}</p>
          <a
            href={`${GITHUB_REPO_URL}/graphs/contributors`}
            target="_blank"
            rel="noopener noreferrer"
            className={cn(buttonVariants({ variant: "outline" }))}
          >
            {copy.viewAll}
          </a>
        </div>
      ) : (
        <>
          <div className="mx-auto grid max-w-5xl grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
            {contributors.map((person) => (
              <a
                key={person.login}
                href={person.htmlUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex flex-col items-center rounded-2xl border border-border bg-card p-4 text-center shadow-xs transition-colors hover:border-brand/40 hover:bg-muted/30"
              >
                <Avatar className="size-16 ring-1 ring-input">
                  <AvatarImage
                    src={person.avatarUrl}
                    alt={person.login}
                    className="aspect-square size-full object-cover"
                  />
                  <AvatarFallback className="bg-muted text-sm font-medium">
                    {person.login.slice(0, 2).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <p className="mt-3 w-full truncate text-sm font-semibold text-foreground">
                  {person.login}
                </p>
                <p className="mt-1 text-xs text-muted-foreground tabular-nums">
                  {person.contributions} {copy.commits}
                </p>
              </a>
            ))}
          </div>

          <div className="mt-10 flex justify-center">
            <a
              href={`${GITHUB_REPO_URL}/graphs/contributors`}
              target="_blank"
              rel="noopener noreferrer"
              className={cn(buttonVariants({ variant: "outline", size: "lg" }))}
            >
              {copy.viewAll}
            </a>
          </div>
        </>
      )}
    </section>
  );
}
