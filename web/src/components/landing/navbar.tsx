"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Github, Menu } from "lucide-react";
import { Button, buttonVariants } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Separator } from "@/components/ui/separator";
import ThemeToggle from "@/components/layout/header/components/theme-toggle";
import LanguageToggle from "@/components/layout/header/components/language-toggle";
import { cn } from "@/lib/utils";
import { GITHUB_REPO_URL } from "@/lib/github";
import { useI18n } from "@/i18n/provider";

const X_URL = "https://x.com/vudovn354";

const XIcon = ({ className }: { className?: string }) => (
  <svg
    viewBox="0 0 24 24"
    fill="currentColor"
    className={className}
    aria-hidden="true"
  >
    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
  </svg>
);

const routeKeys = [
  { href: "#benefits", key: "benefits" },
  { href: "#features", key: "features" },
  { href: "#workflows", key: "workflows" },
  { href: "#testimonials", key: "testimonials" },
  { href: "#sponsored", key: "sponsored" },
  { href: "#contribute", key: "contribute" },
  { href: "#faq", key: "faq" },
] as const;

export function LandingNavbar() {
  const [open, setOpen] = useState(false);
  const { t } = useI18n();
  const landing = t.landing;
  const routes = routeKeys.map(({ href, key }) => ({
    href,
    label: landing.nav[key],
  }));

  return (
    <header className="sticky top-5 z-40 mx-auto flex w-[92%] items-center justify-between rounded-2xl border border-border bg-card/90 p-2 shadow-sm backdrop-blur md:w-[80%] lg:max-w-screen-xl">
      <Link href="/" className="flex items-center gap-2 px-2 font-bold text-lg">
        <Image
          src="/images/logo.png"
          alt="AG Kit"
          width={36}
          height={36}
          className="size-9 rounded-lg"
          priority
        />
        AG Kit
      </Link>

      <div className="flex items-center lg:hidden">
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger
            render={
              <Button variant="ghost" size="icon" aria-label="Open menu" />
            }
          >
            <Menu className="size-5" />
          </SheetTrigger>
          <SheetContent side="left" className="rounded-r-2xl border-border bg-card">
            <SheetHeader className="mb-2">
              <SheetTitle className="flex items-center gap-2">
                <Image
                  src="/images/logo.png"
                  alt="AG Kit"
                  width={32}
                  height={32}
                  className="size-8 rounded-lg"
                />
                AG Kit
              </SheetTitle>
            </SheetHeader>

            <nav className="flex flex-col gap-1 px-4">
              {routes.map(({ href, label }) => (
                <Link
                  key={href}
                  href={href}
                  onClick={() => setOpen(false)}
                  className={cn(
                    buttonVariants({ variant: "ghost" }),
                    "justify-start text-base",
                  )}
                >
                  {label}
                </Link>
              ))}
              <Link
                href="/docs"
                onClick={() => setOpen(false)}
                className={cn(
                  buttonVariants({ variant: "ghost" }),
                  "justify-start text-base",
                )}
              >
                {landing.nav.docs}
              </Link>
              <Link
                href="/orbital-lab"
                onClick={() => setOpen(false)}
                className="flex items-center gap-2 px-3 py-2 rounded-lg font-mono text-sm font-bold text-cyan-400 bg-cyan-950/40 border border-cyan-500/40"
              >
                <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
                🛸 Orbital Paper Lab
              </Link>
            </nav>

            <SheetFooter variant="bare" className="mt-auto flex-col items-start gap-3">
              <Separator />
              <div className="flex items-center gap-2">
                <LanguageToggle />
                <ThemeToggle />
                <Link
                  href={X_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="X / Twitter @vudovn354"
                  className={cn(buttonVariants({ variant: "ghost", size: "icon" }))}
                >
                  <XIcon className="size-4" />
                </Link>
                <Link
                  href={GITHUB_REPO_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="GitHub"
                  className={cn(buttonVariants({ variant: "ghost", size: "icon" }))}
                >
                  <Github className="size-5" />
                </Link>
              </div>
            </SheetFooter>
          </SheetContent>
        </Sheet>
      </div>

      <nav className="mx-auto hidden items-center gap-1 lg:flex">
        {routes.map(({ href, label }) => (
          <Link
            key={href}
            href={href}
            className="rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
          >
            {label}
          </Link>
        ))}
        <Link
          href="/docs"
          className="rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
        >
          {landing.nav.docs}
        </Link>
        <Link
          href="/orbital-lab"
          className="inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-mono font-bold text-cyan-400 bg-cyan-950/60 border border-cyan-500/40 hover:bg-cyan-900/60 transition-all shadow-[0_0_10px_rgba(6,182,212,0.2)]"
        >
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
          🛸 ORBITAL LAB
        </Link>
      </nav>

      <div className="hidden items-center gap-1 lg:flex">
        <LanguageToggle />
        <ThemeToggle />
        <Link
          href={X_URL}
          target="_blank"
          rel="noopener noreferrer"
          aria-label="X / Twitter @vudovn354"
          className={cn(buttonVariants({ variant: "ghost", size: "icon" }))}
        >
          <XIcon className="size-4" />
        </Link>
        <Link
          href={GITHUB_REPO_URL}
          target="_blank"
          rel="noopener noreferrer"
          aria-label="GitHub"
          className={cn(buttonVariants({ variant: "ghost", size: "icon" }))}
        >
          <Github className="size-5" />
        </Link>
      </div>
    </header>
  );
}
