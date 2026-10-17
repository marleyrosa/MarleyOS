"use client";

import { useI18n } from "@/i18n/provider";

interface LocalizedDocProps {
    en: React.ReactNode;
    vi?: React.ReactNode;
    zh?: React.ReactNode;
    ja?: React.ReactNode;
}

/**
 * Picks the MDX content matching the active locale, falling back to English
 * when a translation for the active locale hasn't been authored yet.
 * Every branch passed in is rendered server-side; this only chooses which to
 * display, so language switches happen instantly without a reload.
 */
export default function LocalizedDoc({ en, vi, zh, ja }: LocalizedDocProps) {
    const { locale } = useI18n();
    const byLocale = { en, vi, zh, ja };
    return <>{byLocale[locale] ?? en}</>;
}
