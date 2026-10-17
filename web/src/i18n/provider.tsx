"use client";

import { createContext, useContext, useEffect, useSyncExternalStore } from "react";
import {
    subscribe,
    getStoredLocale,
    getServerLocale,
    setStoredLocale,
    type Locale,
} from "./locale-store";
import { dictionaries, type Dictionary } from "./dictionaries";

interface I18nValue {
    locale: Locale;
    t: Dictionary;
    setLocale: (next: Locale) => void;
}

const I18nContext = createContext<I18nValue | null>(null);

export function I18nProvider({ children }: { children: React.ReactNode }) {
    const locale = useSyncExternalStore(subscribe, getStoredLocale, getServerLocale);

    // Keep <html lang> in sync so screen readers pick the right language.
    useEffect(() => {
        document.documentElement.lang = locale;
    }, [locale]);

    const value: I18nValue = {
        locale,
        t: dictionaries[locale],
        setLocale: setStoredLocale,
    };

    return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n(): I18nValue {
    const ctx = useContext(I18nContext);
    if (!ctx) {
        // Fallback so components used outside the provider still render (English).
        return {
            locale: "en",
            t: dictionaries.en,
            setLocale: setStoredLocale,
        };
    }
    return ctx;
}
