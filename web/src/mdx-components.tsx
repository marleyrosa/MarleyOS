import type { MDXComponents } from "mdx/types";
import Link from "next/link";
import MdxPre from "@/components/docs/mdx-pre";

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    pre: (props) => <MdxPre {...props} />,
    h1: ({ children, id }) => (
      <h1 id={id} className="text-4xl font-bold tracking-tight text-foreground mb-2 scroll-mt-20">
        {children}
      </h1>
    ),
    h2: ({ children, id }) => (
      <h2 id={id} className="text-2xl font-semibold text-foreground mb-4 mt-8 scroll-mt-20">
        {children}
      </h2>
    ),
    h3: ({ children, id }) => (
      <h3 id={id} className="text-xl font-semibold text-foreground mb-3 mt-6 scroll-mt-20">
        {children}
      </h3>
    ),
    h4: ({ children, id }) => (
      <h4 id={id} className="text-lg font-semibold text-foreground mb-2 mt-4 scroll-mt-20">
        {children}
      </h4>
    ),
    p: ({ children }) => (
      <p className="text-muted-foreground leading-relaxed mb-4">{children}</p>
    ),
    a: ({ href, children, className, ...props }) => {
      // rehype-autolink-headings wraps title text in <a class="heading-anchor">.
      // Those must inherit the heading color, not look like brand links.
      const classNames = Array.isArray(className)
        ? className.join(" ")
        : typeof className === "string"
          ? className
          : "";
      if (classNames.includes("heading-anchor")) {
        return (
          <a
            href={href}
            className="heading-anchor text-inherit no-underline hover:text-inherit"
            {...props}
          >
            {children}
          </a>
        );
      }

      const isExternal = href?.startsWith("http");
      if (isExternal) {
        return (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-brand hover:underline underline-offset-4"
            {...props}
          >
            {children}
          </a>
        );
      }
      return (
        <Link
          href={href || "#"}
          className="text-brand hover:underline underline-offset-4"
        >
          {children}
        </Link>
      );
    },
    ul: ({ children }) => (
      <ul className="list-disc list-outside pl-5 text-muted-foreground space-y-1.5 mb-4 marker:text-muted-foreground">
        {children}
      </ul>
    ),
    ol: ({ children }) => (
      <ol className="list-decimal list-outside pl-5 text-muted-foreground space-y-1.5 mb-4 marker:text-muted-foreground">
        {children}
      </ol>
    ),
    li: ({ children }) => <li className="pl-1">{children}</li>,
    // Inline code only. Fenced code blocks are wrapped by rehype-pretty-code
    // in a <pre> (styled via globals.css), so this never double-boxes them.
    code: ({ children }) => (
      <code className="px-1.5 py-0.5 rounded bg-muted text-[0.85em] font-mono text-brand">
        {children}
      </code>
    ),
    blockquote: ({ children }) => (
      <blockquote className="border-l-2 border-brand/40 bg-brand/5 rounded-r px-4 py-2 text-muted-foreground mb-4 [&>p]:mb-0">
        {children}
      </blockquote>
    ),
    hr: () => <hr className="border-border my-8" />,
    table: ({ children }) => (
      <div className="overflow-x-auto mb-4 rounded-lg border border-border">
        <table className="min-w-full divide-y divide-border">
          {children}
        </table>
      </div>
    ),
    th: ({ children }) => (
      <th className="px-4 py-2 text-left text-sm font-semibold text-foreground bg-muted">
        {children}
      </th>
    ),
    td: ({ children }) => (
      <td className="px-4 py-2 text-sm text-muted-foreground border-t border-border">
        {children}
      </td>
    ),
    ...components,
  };
}
