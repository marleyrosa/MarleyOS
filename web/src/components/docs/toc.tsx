"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useI18n } from "@/i18n/provider";

interface Heading {
  id: string;
  text: string;
  level: number;
}

export default function Toc() {
  const { t, locale } = useI18n();
  const pathname = usePathname();
  const [headings, setHeadings] = useState<Heading[]>([]);
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    const main = document.querySelector("main");
    if (!main) return;

    const slugify = (text: string) =>
      text
        .toLowerCase()
        .trim()
        .replace(/[^\p{L}\p{N}\s-]/gu, "")
        .replace(/\s+/g, "-")
        .replace(/-+/g, "-");

    const nodes = Array.from(
      main.querySelectorAll<HTMLElement>("h2, h3")
    );
    // Ensure every heading has an id so it can be linked/observed (covers
    // hardcoded .tsx pages where rehype-slug never ran).
    const seen = new Set<string>();
    nodes.forEach((node) => {
      if (!node.id) {
        const base = slugify(node.textContent ?? "") || "section";
        let id = base;
        let n = 1;
        while (seen.has(id)) id = `${base}-${n++}`;
        node.id = id;
      }
      seen.add(node.id);
    });

    const items: Heading[] = nodes.map((node) => ({
      id: node.id,
      text: node.textContent ?? "",
      level: Number(node.tagName[1]),
    }));

    const frameId = window.requestAnimationFrame(() => {
      setHeadings(items);
    });

    if (items.length === 0) {
      return () => window.cancelAnimationFrame(frameId);
    }

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        }
      },
      { rootMargin: "0px 0px -80% 0px", threshold: 1.0 }
    );

    nodes.forEach((node) => observer.observe(node));
    return () => {
      window.cancelAnimationFrame(frameId);
      observer.disconnect();
    };
  }, [pathname, locale]);

  if (headings.length === 0) {
    return (
      <div className="text-xs text-muted-foreground">
        {t.toc.empty}
      </div>
    );
  }

  return (
    <nav>
      <div className="font-semibold text-foreground mb-3">
        {t.toc.onThisPage}
      </div>
      <ul className="space-y-2 text-sm border-l border-border">
        {headings.map((h) => (
          <li key={h.id} style={{ paddingLeft: h.level === 3 ? "1.25rem" : "0.75rem" }}>
            <a
              href={`#${h.id}`}
              className={cn(
                "block -ml-px border-l-2 pl-3 py-0.5 transition-colors",
                activeId === h.id
                  ? "border-brand text-brand font-medium"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              )}
            >
              {h.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
