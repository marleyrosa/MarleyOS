# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

AG Kit is an Antigravity-first AI agent engineering kit. The product is the `.agents/` workspace contract itself (rules, skills, agents, workflows, memory, hooks) — Markdown + JSON consumed by the Google Antigravity runtime, not compiled code. Three deliverables live in one repo:

- `.agents/` — the toolkit: 20 specialist agents (`agent/`), ~50 skills (`skills/`), 13 slash-command workflows (`workflows/`), 6 rules (`rules/`), persistent memory templates (`memory/`), plus the Antigravity runtime layer (`antigravity.json` contract, `hooks.json` PreToolUse safety gate, `hooks/*.mjs` tooling, JSON schemas).
- `cli/` — published npm package `@vudovn/ag-kit` (Node ≥18, ESM). Installs the kit into user projects via `giget`. Entry: `cli/bin/index.js`, managed-tree logic in `cli/lib/managed-tree.js`.
- `web/` — docs site (Next.js 16 + MDX + Tailwind 4, React 19). Content data lives in JSON catalogs under `web/src`.

Python ≥3.10 (with PyYAML) runs the toolkit validators; Node ≥22 runs the Antigravity tooling.

## Commands

All from repo root unless noted.

```bash
# Toolkit (.agents/) — run after ANY change to managed components
npm run generate:agents      # regenerate manifest.json, manifest.lock.json, DEPENDENCY_GRAPH.md
npm run check:agents         # manifest --check + graph --check + validate_kit.py (what CI runs)
npm run test:toolkit         # python -m unittest discover -s .agents/scripts/tests -v

# Antigravity runtime layer
npm run check:antigravity    # doctor: validates contract, hooks, schemas
npm run test:antigravity     # node --test .agents/hooks/tests/antigravity.test.mjs
npm run build:antigravity-plugin

# CLI
npm run test:cli             # or: cd cli && node --test test/*.test.js
node --test cli/test/managed-tree.test.js   # single test file

# Web (deps installed per-package: npm ci in cli/ and web/)
npm run lint:web
npm run typecheck:web
npm run build:web            # next build --webpack (not turbopack)
```

Single Python test: `python -m unittest .agents.scripts.tests.test_toolkit -v` won't work due to path; use `python -m unittest discover -s .agents/scripts/tests -k <pattern> -v`.

## The managed component registry (critical)

Any edit to a managed component (files in `.agents/agent|skills|workflows|rules`, hooks, schemas) **must** be followed by `npm run generate:agents`, or `check:agents` and CI fail on hash mismatch. Never hand-edit `manifest.json`, `manifest.lock.json`, or `DEPENDENCY_GRAPH.md` — all generated.

Dual-track versioning:
- Toolkit releases: **CalVer** `YYYY.M.D` in `.agents/VERSION`.
- Individual components: **SemVer** in their Markdown frontmatter. Bump the component's frontmatter version when changing it.

## Component conventions

- Agents, skills, workflows, and rules are Markdown with YAML frontmatter (`name`, `description`, `version`, plus `tools`/`dependencies` where applicable). Frontmatter shape is validated by `validate_kit.py` — match existing files in the same directory.
- Skills use progressive/conditional loading ("Selective Reading"): a short always-loaded core with deeper sections loaded on demand. Keep new skill content in that shape.
- Cross-component dependencies are declared in frontmatter and materialize in the generated dependency graph; a dangling dependency fails `check:agents`.
- The native PreToolUse hook (`hooks.json` + `validate-tool-call.mjs`) is deliberately narrow: blocks root-filesystem deletion, drive formatting, raw-disk writes only. Don't broaden it into a general linter.

## Release

- Version is CalVer and must be synced across **three** `package.json` files (root, `cli/`, `web/`) plus `.agents/VERSION`. `cli/test/release-safety.test.js` guards this.
- npm publish runs via `.github/workflows/publish.yml`; CI (`ci.yml`) runs toolkit validation, CLI tests + `npm pack --dry-run` + prod audit, and web lint/typecheck/build/audit. `antigravity.yml` runs doctor, hook tests, and plugin build.

## Web notes

- `next build --webpack` is intentional: the MDX plugin config breaks under Turbopack unless plugins are referenced by string name (see `web/next.config.ts`).
- Docs content is driven by JSON catalog data under `web/src`, not by scanning `.agents/` at build time — update the catalogs when components change.
