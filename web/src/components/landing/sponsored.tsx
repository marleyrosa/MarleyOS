"use client";

import Image from "next/image";
import Link from "next/link";
import { ExternalLink, HeartHandshake } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { useI18n } from "@/i18n/provider";
import { cn } from "@/lib/utils";

const SPONSOR_URL = "https://unikorn.vn/";
const SPONSOR_INQUIRE = "https://github.com/vudovn";

export function LandingSponsored() {
  const { t } = useI18n();
  const copy = t.landing.sponsored;

  return (
    <section
      id="sponsored"
      className="container mx-auto px-4 py-20 sm:px-6 sm:py-28 lg:px-8"
    >
      <p className="mb-2 text-center text-lg tracking-wider text-brand">
        {copy.eyebrow}
      </p>
      <h2 className="mb-4 text-center text-3xl font-bold tracking-tight md:text-4xl">
        {copy.title}
      </h2>
      <p className="mx-auto mb-12 max-w-2xl text-center text-lg text-muted-foreground">
        {copy.subtitle}
      </p>

      <div className="mx-auto grid max-w-5xl gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <a
          href={SPONSOR_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-border bg-card p-8 shadow-xs transition-colors hover:border-brand/40"
        >
          <div className="absolute inset-0 bg-gradient-to-br from-brand/10 via-transparent to-transparent opacity-80" />
          <div className="relative">
            <div className="mb-4 flex items-center gap-4">
              <div className="flex size-14 items-center justify-center rounded-xl border border-border bg-background">
                <svg
                  width={32}
                  height={32}
                  viewBox="0 0 1000 1000"
                  fill="currentColor"
                  className="text-foreground"
                  aria-hidden
                >
                  <g transform="matrix(1,0,0,1,0,9.204355)">
                    <path d="M890.828,5.864C895.373,4.486 900.302,5.343 904.116,8.172C907.93,11.002 910.178,15.47 910.178,20.219C910.178,143.585 910.178,795.144 910.178,961.372C910.178,967.476 906.48,972.971 900.825,975.269C895.17,977.566 888.687,976.208 884.429,971.834C645.13,726.029 399.028,922.802 198.646,716.77C128.914,644.809 89.922,548.538 89.922,448.334C89.822,333.557 89.822,156.891 89.822,111.128C89.822,104.519 94.147,98.689 100.472,96.773C147.714,82.457 338.731,24.573 400.472,5.864C405.016,4.486 409.945,5.343 413.759,8.172C417.573,11.002 419.822,15.47 419.822,20.219C419.822,92.456 419.822,340.356 419.822,469.822C419.822,514.103 455.719,550 500,550L500,550C544.281,550 580.178,514.103 580.178,469.822L580.178,111.128C580.178,104.519 584.504,98.689 590.828,96.773C638.071,82.457 829.088,24.573 890.828,5.864Z" />
                  </g>
                </svg>
              </div>
              <div>
                <h3 className="text-2xl font-semibold tracking-tight">
                  Unikorn
                </h3>
                <p className="text-sm text-muted-foreground">unikorn.vn</p>
              </div>
            </div>
            <p className="max-w-xl leading-relaxed text-muted-foreground">
              {copy.unikornBlurb}
            </p>
          </div>
          <div className="relative mt-8 inline-flex items-center gap-2 text-sm font-medium text-brand">
            {copy.visitSponsor}
            <ExternalLink className="size-4 transition-transform group-hover:translate-x-0.5" />
          </div>
        </a>

        <div className="flex flex-col justify-between rounded-2xl border border-dashed border-border bg-muted/30 p-8">
          <div>
            <div className="mb-4 flex size-12 items-center justify-center rounded-full bg-brand/15 text-brand">
              <HeartHandshake className="size-6" />
            </div>
            <h3 className="mb-2 text-xl font-semibold">{copy.becomeTitle}</h3>
            <p className="text-sm leading-relaxed text-muted-foreground">
              {copy.becomeDesc}
            </p>
          </div>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row lg:flex-col">
            <a
              href={SPONSOR_INQUIRE}
              target="_blank"
              rel="noopener noreferrer"
              className={cn(
                buttonVariants({ size: "lg" }),
                "w-full sm:w-auto lg:w-full",
              )}
            >
              {copy.talk}
            </a>
            <Link
              href="https://buymeacoffee.com/vudovn"
              target="_blank"
              rel="noopener noreferrer"
              className={cn(
                buttonVariants({ size: "lg", variant: "outline" }),
                "w-full sm:w-auto lg:w-full",
              )}
            >
              {copy.coffee}
            </Link>
          </div>
        </div>
      </div>

      <div className="mx-auto mt-10 flex max-w-5xl flex-wrap items-center justify-center gap-3 text-sm text-muted-foreground">
        <Image
          src="/images/logo.png"
          alt=""
          width={20}
          height={20}
          className="size-5 rounded opacity-70"
        />
        <span>
          {copy.wantBrand}{" "}
          <a
            href={SPONSOR_INQUIRE}
            target="_blank"
            rel="noopener noreferrer"
            className="font-medium text-foreground underline-offset-4 hover:text-brand hover:underline"
          >
            {copy.reachOut}
          </a>
          .
        </span>
      </div>
    </section>
  );
}
