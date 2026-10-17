'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { docsNavFlat } from '@/lib/docs-nav';
import { useI18n } from '@/i18n/provider';

export default function DocsPager() {
    const pathname = usePathname();
    const { t } = useI18n();
    const searchDict = t.search as unknown as Record<string, string>;

    const index = docsNavFlat.findIndex((item) => item.href === pathname);
    if (index === -1) return null;

    const prev = docsNavFlat[index - 1];
    const next = docsNavFlat[index + 1];
    const label = (item: (typeof docsNavFlat)[number]) =>
        (item.labelKey && searchDict[item.labelKey]) || item.label;

    return (
        <nav
            aria-label="Docs pagination"
            className="mt-12 pt-6 border-t border-border flex items-stretch justify-between gap-4"
        >
            {prev ? (
                <Link
                    href={prev.href}
                    className="group flex-1 max-w-[48%] p-4 rounded-lg border border-border hover:bg-muted transition-colors"
                >
                    <div className="text-xs text-muted-foreground mb-1">←</div>
                    <div className="text-sm font-medium text-foreground group-hover:text-brand transition-colors">
                        {label(prev)}
                    </div>
                </Link>
            ) : (
                <span className="flex-1 max-w-[48%]" />
            )}
            {next ? (
                <Link
                    href={next.href}
                    className="group flex-1 max-w-[48%] p-4 rounded-lg border border-border hover:bg-muted transition-colors text-right"
                >
                    <div className="text-xs text-muted-foreground mb-1">→</div>
                    <div className="text-sm font-medium text-foreground group-hover:text-brand transition-colors">
                        {label(next)}
                    </div>
                </Link>
            ) : (
                <span className="flex-1 max-w-[48%]" />
            )}
        </nav>
    );
}
