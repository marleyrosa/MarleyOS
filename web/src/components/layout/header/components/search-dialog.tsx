'use client';

import { Fragment, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowDownIcon, ArrowUpIcon, CornerDownLeftIcon, FileTextIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
    Command,
    CommandCollection,
    CommandDialog,
    CommandDialogPopup,
    CommandDialogTrigger,
    CommandEmpty,
    CommandFooter,
    CommandGroup,
    CommandGroupLabel,
    CommandInput,
    CommandItem,
    CommandList,
    CommandPanel,
    CommandSeparator,
} from '@/components/ui/command';
import { Kbd, KbdGroup } from '@/components/ui/kbd';
import { useI18n } from '@/i18n/provider';

import { docsNav, type DocsNavItem, type DocsNavSection } from '@/lib/docs-nav';

type SearchItem = DocsNavItem;
type SearchGroup = DocsNavSection;

const searchGroups: SearchGroup[] = docsNav;

export default function SearchDialog() {
    const [open, setOpen] = useState(false);
    const router = useRouter();
    const { t } = useI18n();

    function handleItemClick(item: SearchItem) {
        router.push(item.href);
        setOpen(false);
    }

    useEffect(() => {
        const down = (e: KeyboardEvent) => {
            if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                setOpen((open) => !open);
            }
        };

        document.addEventListener('keydown', down);
        return () => document.removeEventListener('keydown', down);
    }, []);

    return (
        <CommandDialog onOpenChange={setOpen} open={open}>
            {/* Mobile/Tablet - Icon Only */}
            <CommandDialogTrigger
                className="md:hidden"
                render={
                    <Button
                        variant="ghost"
                        size="icon"
                        aria-label="Search"
                    />
                }
            >
                <svg className="w-4 h-4 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
            </CommandDialogTrigger>

            {/* Desktop - Full Search Input */}
            <CommandDialogTrigger
                className="hidden md:flex bg-transparent"
                render={
                    <Button
                        variant="outline"
                        className="w-full justify-start text-sm text-muted-foreground font-normal h-9"
                    />
                }
            >
                <svg className="w-4 h-4 mr-2 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span className="flex-1 text-left">{t.search.placeholder}</span>
                <KbdGroup className="hidden sm:inline-flex">
                    <Kbd>⌘</Kbd>
                    <Kbd>K</Kbd>
                </KbdGroup>
            </CommandDialogTrigger>

            <CommandDialogPopup>
                <Command items={searchGroups}>
                    <CommandInput placeholder={t.search.inputPlaceholder} />
                    <CommandPanel>
                        <CommandEmpty>
                            <div className="flex flex-col items-center justify-center py-6 text-center">
                                <svg className="w-10 h-10 text-muted-foreground/30 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <p className="text-sm font-medium text-foreground mb-1">{t.search.noResults}</p>
                                <p className="text-xs text-muted-foreground">{t.search.noResultsHint}</p>
                            </div>
                        </CommandEmpty>
                        <CommandList>
                            {(group: SearchGroup) => (
                                <Fragment key={group.title}>
                                    <CommandGroup items={group.items}>
                                        <CommandGroupLabel>{(group.titleKey && (t.search as unknown as Record<string, string>)[group.titleKey]) || group.title}</CommandGroupLabel>
                                        <CommandCollection>
                                            {(item: SearchItem) => (
                                                <CommandItem
                                                    key={item.href}
                                                    onClick={() => handleItemClick(item)}
                                                    value={item.label + ' ' + (item.keywords || '')}
                                                >
                                                    <FileTextIcon className="mr-2 h-4 w-4 text-muted-foreground" />
                                                    <span className="flex-1">{(item.labelKey && (t.search as unknown as Record<string, string>)[item.labelKey]) || item.label}</span>
                                                    <span className="text-xs text-muted-foreground">{item.href}</span>
                                                </CommandItem>
                                            )}
                                        </CommandCollection>
                                    </CommandGroup>
                                    <CommandSeparator />
                                </Fragment>
                            )}
                        </CommandList>
                    </CommandPanel>
                    <CommandFooter>
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2">
                                <KbdGroup>
                                    <Kbd>
                                        <ArrowUpIcon className="h-3 w-3" />
                                    </Kbd>
                                    <Kbd>
                                        <ArrowDownIcon className="h-3 w-3" />
                                    </Kbd>
                                </KbdGroup>
                                <span className="text-xs text-muted-foreground">{t.search.navigate}</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <Kbd>
                                    <CornerDownLeftIcon className="h-3 w-3" />
                                </Kbd>
                                <span className="text-xs text-muted-foreground">{t.search.select}</span>
                            </div>
                        </div>
                        <div className="flex items-center gap-2">
                            <Kbd>Esc</Kbd>
                            <span className="text-xs text-muted-foreground">{t.search.close}</span>
                        </div>
                    </CommandFooter>
                </Command>
            </CommandDialogPopup>
        </CommandDialog>
    );
}
