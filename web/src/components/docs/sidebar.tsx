'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { docsNav } from '@/lib/docs-nav';
import { useI18n } from '@/i18n/provider';

export default function DocsSidebar() {
    const pathname = usePathname();
    const { t } = useI18n();
    const searchDict = t.search as unknown as Record<string, string>;

    return (
        <nav className="space-y-1">
            {docsNav.map((section) => (
                <div key={section.title} className="pb-6">
                    <h3 className="mb-3 px-2 text-sm font-semibold text-foreground">
                        {(section.titleKey && searchDict[section.titleKey]) || section.title}
                    </h3>
                    <div className="space-y-0.5">
                        {section.items.map((item) => {
                            const isActive = pathname === item.href;
                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={`
                    block px-2 py-1.5 text-sm rounded-md transition-colors
                    ${isActive
                                            ? 'bg-brand/10 text-brand font-medium'
                                            : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                                        }
                  `}
                                >
                                    {(item.labelKey && searchDict[item.labelKey]) || item.label}
                                </Link>
                            );
                        })}
                    </div>
                </div>
            ))}
        </nav>
    );
}
