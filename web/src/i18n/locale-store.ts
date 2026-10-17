"use client";

export const LOCALE_KEY = "ag-kit-locale";
export const LOCALES = ["en", "vi", "zh", "ja"] as const;
export type Locale = (typeof LOCALES)[number];

export function isLocale(value: string | null | undefined): value is Locale {
    return value === "en" || value === "vi" || value === "zh" || value === "ja";
}

export function subscribe(callback: () => void) {
    window.addEventListener("storage", callback);
    return () => window.removeEventListener("storage", callback);
}

export function getStoredLocale(): Locale {
    const stored = localStorage.getItem(LOCALE_KEY);
    return isLocale(stored) ? stored : "en";
}

export function getServerLocale(): Locale {
    return "en";
}

export function setStoredLocale(next: Locale) {
    localStorage.setItem(LOCALE_KEY, next);
    // Persist for SSR/middleware to read later when content is localized.
    document.cookie = `${LOCALE_KEY}=${next}; path=/; max-age=31536000; samesite=lax`;
    // storage event only fires cross-tab; dispatch manually for same-tab listeners.
    window.dispatchEvent(new Event("storage"));
}
