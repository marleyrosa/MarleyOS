'use client';

import { useRef, useState } from 'react';
import { CheckIcon, CopyIcon } from 'lucide-react';

// Wraps rehype-pretty-code fenced blocks to add a copy button.
export default function MdxPre(props: React.ComponentPropsWithoutRef<'pre'>) {
    const preRef = useRef<HTMLPreElement>(null);
    const [copied, setCopied] = useState(false);

    const copy = async () => {
        const text = preRef.current?.innerText ?? '';
        await navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="relative group">
            <pre ref={preRef} {...props} />
            <button
                onClick={copy}
                className="absolute top-3 right-3 p-2 rounded-md border border-code-border bg-code-title text-code-foreground transition-colors opacity-0 group-hover:opacity-100 focus-visible:opacity-100 hover:bg-code-border"
                aria-label="Copy code"
            >
                {copied ? (
                    <CheckIcon className="w-4 h-4 text-brand" />
                ) : (
                    <CopyIcon className="w-4 h-4 text-code-foreground/70" />
                )}
            </button>
        </div>
    );
}
