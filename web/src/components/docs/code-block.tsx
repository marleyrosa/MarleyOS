'use client';

import { useState } from 'react';
import { CheckIcon, CopyIcon } from 'lucide-react';

interface CodeBlockProps {
    code: string;
    language?: string;
    showLineNumbers?: boolean;
    className?: string;
}

export function CodeBlock({ code, language = 'bash', showLineNumbers = false, className }: CodeBlockProps) {
    const [copied, setCopied] = useState(false);

    const copyToClipboard = async () => {
        await navigator.clipboard.writeText(code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className={`relative group ${className}`}>
            <pre className={`p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm ${showLineNumbers ? 'pl-12' : ''}`}>
                <code className="text-code-foreground" data-language={language}>{code}</code>
            </pre>
            <button
                onClick={copyToClipboard}
                className="absolute top-3 right-3 p-2 rounded-md border border-code-border bg-code-title text-code-foreground transition-colors opacity-0 group-hover:opacity-100 hover:bg-code-border"
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
