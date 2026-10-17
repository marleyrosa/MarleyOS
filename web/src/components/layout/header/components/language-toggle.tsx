'use client';

import Image from 'next/image';
import { Button } from '../../../ui/button';
import {
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuRadioGroup,
    DropdownMenuRadioItem,
} from '../../../ui/menu';
import { useI18n } from '@/i18n/provider';
import type { Locale } from '@/i18n/locale-store';

const LOCALES = [
    { value: 'en', label: 'English', flag: '/flags/gb.svg' },
    { value: 'vi', label: 'Tiếng Việt', flag: '/flags/vn.svg' },
    { value: 'zh', label: '中文', flag: '/flags/cn.svg' },
    { value: 'ja', label: '日本語', flag: '/flags/jp.svg' },
] as const;

export default function LanguageToggle() {
    const { locale, setLocale } = useI18n();
    const current = LOCALES.find((l) => l.value === locale) ?? LOCALES[0];

    return (
        <DropdownMenu>
            <DropdownMenuTrigger
                render={
                    <Button variant="ghost" size="icon" aria-label="Select language">
                        <Image
                            src={current.flag}
                            alt={current.label}
                            width={20}
                            height={14}
                            className="w-5 h-auto rounded-[2px]"
                        />
                    </Button>
                }
            />
            <DropdownMenuContent align="end" className="min-w-36">
                <DropdownMenuRadioGroup
                    value={locale}
                    onValueChange={(v) => setLocale(v as Locale)}
                >
                    {LOCALES.map((l) => (
                        <DropdownMenuRadioItem key={l.value} value={l.value}>
                            <span className="flex items-center gap-2">
                                <Image
                                    src={l.flag}
                                    alt=""
                                    width={20}
                                    height={14}
                                    className="w-5 h-auto rounded-[2px] shrink-0"
                                />
                                {l.label}
                            </span>
                        </DropdownMenuRadioItem>
                    ))}
                </DropdownMenuRadioGroup>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
