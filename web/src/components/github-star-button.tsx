"use client";

import { Github, Star } from "lucide-react";
import type { VariantProps } from "class-variance-authority";
import { buttonVariants } from "@/components/ui/button";
import { useGithubStars } from "@/hooks/use-github-stars";
import { formatStarCount, GITHUB_REPO_URL } from "@/lib/github";
import { cn } from "@/lib/utils";

type ButtonVariant = VariantProps<typeof buttonVariants>["variant"];
type ButtonSize = VariantProps<typeof buttonVariants>["size"];

type GithubStarButtonProps = {
  className?: string;
  variant?: ButtonVariant;
  size?: ButtonSize;
  label?: string;
};

/** GitHub CTA with live star count (hero / marketing only — not used on headers). */
export function GithubStarButton({
  className,
  variant = "secondary",
  size = "lg",
  label = "GitHub",
}: GithubStarButtonProps) {
  const { stars } = useGithubStars();
  const starLabel = stars != null ? formatStarCount(stars) : null;

  return (
    <a
      href={GITHUB_REPO_URL}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={
        starLabel ? `GitHub, ${stars} stars` : "GitHub repository"
      }
      className={cn(
        buttonVariants({ variant, size }),
        "font-semibold",
        className,
      )}
    >
      <Github className="size-5" />
      <span>{label}</span>
      {starLabel ? (
        <>
          <span className="text-muted-foreground" aria-hidden>
            ·
          </span>
          <span className="inline-flex items-center gap-1 tabular-nums">
            <Star className="size-3.5 fill-current text-brand" aria-hidden />
            {starLabel}
          </span>
        </>
      ) : null}
    </a>
  );
}
