'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import DonateDialog from '@/components/layout/header/components/donate-dialog';
import { GithubIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useI18n } from '@/i18n/provider';

import { docsNav } from '@/lib/docs-nav';

export default function MobileMenu() {
    const [isOpen, setIsOpen] = useState(false);
    const pathname = usePathname();
    const { t } = useI18n();

    return (
        <>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="lg:hidden p-2 rounded-md text-muted-foreground hover:bg-muted transition-colors"
                aria-label="Toggle menu"
            >
                {isOpen ? (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                ) : (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                )}
            </button>

            {isOpen && (
                <div className="lg:hidden absolute left-0 right-0 top-full border-t border-border bg-background shadow-lg animate-in slide-in-from-top-2 max-h-[calc(100vh-3.5rem)] overflow-y-auto">
                    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-6">
                        <nav className="space-y-6">
                            {docsNav.map((section) => (
                                <div key={section.title}>
                                    <h3 className="mb-3 text-sm font-semibold text-foreground">
                                        {(section.titleKey && (t.search as unknown as Record<string, string>)[section.titleKey]) || section.title}
                                    </h3>
                                    <div className="space-y-1">
                                        {section.items.map((item) => {
                                            const isActive = pathname === item.href;
                                            return (
                                                <Link
                                                    key={item.href}
                                                    href={item.href}
                                                    onClick={() => setIsOpen(false)}
                                                    className={`
                                                        block px-3 py-2 text-sm rounded-md transition-colors
                                                        ${isActive
                                                            ? 'bg-brand/10 text-brand font-medium'
                                                            : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                                                        }
                                                    `}
                                                >
                                                    {(item.labelKey && (t.search as unknown as Record<string, string>)[item.labelKey]) || item.label}
                                                </Link>
                                            );
                                        })}
                                    </div>
                                </div>
                            ))}
                        </nav>

                        <div className="mt-6 pt-6 border-t border-border flex gap-3">
                            <DonateDialog className="" />
                            <Link href="https://github.com/vudovn/ag-kit" target="_blank" rel="noopener noreferrer">
                                <Button variant="outline" className="w-full justify-start">
                                    <GithubIcon className="w-4 h-4 mr-2" />
                                    GitHub
                                </Button>
                            </Link>
                            <Link href="https://unikorn.vn/" target="_blank" rel="noopener noreferrer">
                                <Button variant="outline" className="w-full justify-start">
                                    <svg
                                        width={24}
                                        height={24}
                                        viewBox="0 0 1000 1000"
                                        fill="currentColor"
                                        className="shrink-0"
                                        >
                                        <g transform="matrix(1,0,0,1,0,9.204355)">
                                            <path d="M890.828,5.864C895.373,4.486 900.302,5.343 904.116,8.172C907.93,11.002 910.178,15.47 910.178,20.219C910.178,143.585 910.178,795.144 910.178,961.372C910.178,967.476 906.48,972.971 900.825,975.269C895.17,977.566 888.687,976.208 884.429,971.834C645.13,726.029 399.028,922.802 198.646,716.77C128.914,644.809 89.922,548.538 89.922,448.334C89.822,333.557 89.822,156.891 89.822,111.128C89.822,104.519 94.147,98.689 100.472,96.773C147.714,82.457 338.731,24.573 400.472,5.864C405.016,4.486 409.945,5.343 413.759,8.172C417.573,11.002 419.822,15.47 419.822,20.219C419.822,92.456 419.822,340.356 419.822,469.822C419.822,514.103 455.719,550 500,550L500,550C544.281,550 580.178,514.103 580.178,469.822L580.178,111.128C580.178,104.519 584.504,98.689 590.828,96.773C638.071,82.457 829.088,24.573 890.828,5.864Z" />
                                        </g>
                                        </svg>
                                    {t.nav.sponsored}
                                </Button>
                            </Link>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
