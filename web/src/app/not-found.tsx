"use client";

import Link from "next/link";
import { Home, BookOpen } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function NotFound() {
  return (
    <div className="min-h-[100dvh] bg-background text-foreground flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-md text-center space-y-6">
        <div className="inline-flex items-center justify-center size-20 rounded-2xl border border-border bg-muted/50 text-brand text-4xl font-bold font-mono shadow-sm">
          404
        </div>

        <div className="space-y-2">
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">
            Page not found
          </h1>
          <p className="text-sm sm:text-base text-muted-foreground">
            The page or documentation article you are looking for doesn&apos;t exist or has been moved.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <Link
            href="/"
            className={cn(
              buttonVariants({ size: "default" }),
              "w-full sm:w-auto font-semibold gap-2",
            )}
          >
            <Home className="size-4" />
            Home
          </Link>
          <Link
            href="/docs"
            className={cn(
              buttonVariants({ variant: "outline", size: "default" }),
              "w-full sm:w-auto font-semibold gap-2",
            )}
          >
            <BookOpen className="size-4" />
            Documentation
          </Link>
        </div>
      </div>
    </div>
  );
}
