"use client";

import { useEffect, useState } from "react";
import { fetchGithubStars } from "@/lib/github";

/**
 * Live GitHub star count for vudovn/ag-kit.
 * Shared module cache avoids N buttons = N API calls.
 */
export function useGithubStars() {
  const [stars, setStars] = useState<number | null>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let cancelled = false;

    fetchGithubStars().then((count) => {
      if (cancelled) return;
      setStars(count);
      setLoaded(true);
    });

    // Refresh periodically while the page is open.
    const timer = window.setInterval(() => {
      fetchGithubStars().then((count) => {
        if (!cancelled && count != null) setStars(count);
      });
    }, 60_000);

    return () => {
      cancelled = true;
      window.clearInterval(timer);
    };
  }, []);

  return { stars, loaded };
}
