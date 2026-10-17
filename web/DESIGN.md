---
name: AG Kit Web
description: Documentation and marketing site for the AG Kit AI agent toolkit.
colors:
  background: "#FAFAFA"
  foreground: "#18181B"
  card: "#FFFFFF"
  muted: "#F4F4F5"
  muted-foreground: "#71717A"
  border: "#E4E4E7"
  primary: "#18181B"
  primary-foreground: "#FAFAFA"
  brand: "#2DD4BF"
  brand-foreground: "#042F2E"
  destructive: "#EF4444"
  code: "#0C0C0E"
  code-foreground: "#E4E4E7"
  dark-background: "#09090B"
  dark-foreground: "#FAFAFA"
  dark-card: "#0C0C0E"
  dark-muted: "#18181B"
  dark-muted-foreground: "#A1A1AA"
  dark-border: "#27272A"
  dark-primary: "#FAFAFA"
  dark-primary-foreground: "#18181B"
  dark-brand: "#2DD4BF"
typography:
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  headline-lg:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.02em
rounded:
  sm: 6px
  md: 8px
  lg: 10px
  full: 9999px
spacing:
  sm: 8px
  md: 16px
  lg: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-foreground}"
    rounded: "{rounded.lg}"
  brand-mark:
    backgroundColor: "{colors.brand}"
---

# AG Kit Web

## Overview

Technical documentation site for an open-source AI agent toolkit. Visual language is **devtool-clean**: cool zinc neutrals, one teal brand accent taken from the logo (`#2DD4BF`), no multi-color gradients.

Audience: developers installing CLI, reading agents/skills/workflows docs.

## Colors

- **Neutrals:** Zinc family only (cool gray). Light page `#FAFAFA`, dark page `#09090B` (never pure black on marketing chrome).
- **Brand accent:** Teal `#2DD4BF` for links, active TOC, brand wordmarks, terminal prompts. One accent only.
- **Code surfaces:** Near-black `#0C0C0E` in both themes so fenced blocks stay terminal-like.
- **Semantic status:** info blue, success emerald, warning amber, destructive red — used only in callouts/status, not for decoration.

## Typography

Inter system stack for UI; JetBrains Mono / SF Mono for code. Headlines: semibold/bold, tight tracking. Body: relaxed leading, muted-foreground for secondary copy.

## Layout

Docs shell: sticky header 56px, left nav, content max ~4xl, optional right TOC. Home: centered column max-w-3xl. Container padding scales `px-4 sm:px-6 lg:px-8`.

## Elevation & Depth

Prefer 1px borders over heavy shadows. Header uses translucent background + backdrop blur. Cards: border + muted fill, not drop shadows.

## Shapes

Default radius 8–10px. Pills only for primary CTAs on the home page.

## Components

- Buttons use semantic `primary` / `outline` / `ghost`.
- Brand wordmark uses `.brand-mark` (single teal wash), never blue–cyan–orange gradient.
- Inline code: muted chip + brand-colored text.
- Terminal chrome stays dark in both themes.

## Do's and Don'ts

- Do use semantic tokens (`bg-background`, `text-foreground`, `border-border`, `text-muted-foreground`, `text-brand`).
- Do keep light and dark hierarchy parallel.
- Don't hardcode `zinc-*` pairs next to semantic tokens.
- Don't introduce a second accent (blue CTAs, orange highlights) outside status callouts.
- Don't use pure `#000` full-page backgrounds.
