# Migrating AG Kit

This guide covers upgrades across AG Kit releases, including the Antigravity-native runtime layer and subsequent feature releases up to `2026.8.31`.

## Upgrading to `2026.8.31`

### What changes in `2026.8.31`
- **Design Gatekeeper**: `app-builder` now requires a `DESIGN.md` (visual language tokens and rationale) at the project root before frontend implementation begins.
- **AI & Game Application Support**: Added detection for full-stack AI/Chatbot apps (Vercel AI SDK streaming, pgvector) and routed Game development to `game-developer`.
- **Template & CSS Paths**: Standardized `src/app/globals.css` across Next.js templates and updated `@prisma/client` runtime dependencies.
- **Web & SEO**: Schema.org JSON-LD structured data (`SoftwareApplication`, `FAQPage`), Web App Manifest, and custom 404 page.

All existing user code, custom agents, and modified skills are preserved by `ag-kit update` using the default merge strategy.

---

## Migrating to the Antigravity-native runtime (`2026.7.26`+)

The release adds an Antigravity runtime layer:

- `.agents/antigravity.json` — machine-readable runtime contract;
- `.agents/hooks.json` — native Antigravity hook registration;
- `.agents/hooks/` — safety policy, doctor, MCP sync, plugin builder, schemas, and tests;
- Antigravity-specific CI and production documentation.

The only behavior enabled by default is a narrow `PreToolUse` safety gate for the `run_command` tool. It blocks high-confidence root/disk destructive commands and allows ordinary project cleanup.


## Before upgrading

1. Commit or stash project work.
2. Confirm the current AG Kit installation is healthy:

```bash
npm run check:agents
```

3. Preview the update:

```bash
ag-kit update --dry-run
```

4. Review any locally modified `.agents` files shown by the plan.

## Upgrade

```bash
ag-kit update
```

AG Kit creates a backup before changing managed files. It does not silently replace locally modified managed files; conflicts receive an incoming copy and a machine-readable report.

## Post-upgrade validation

```bash
npm run check:agents
npm run check:antigravity
npm run test:antigravity
npm run build:antigravity-plugin
```

Expected result:

- toolkit validation passes;
- Antigravity Doctor reports no errors;
- a warning for `YOUR_API_KEY` is expected until the MCP example is configured;
- Antigravity regression tests pass;
- `dist/antigravity-plugin/` is created successfully.

## Antigravity workspace smoke test

Open the project as a trusted Antigravity workspace and verify:

1. `.agents/rules/`, `.agents/skills/`, and `.agents/workflows/` are discovered;
2. `/coordinate` and `/orchestrate` are available;
3. a normal command such as `npm test` is allowed;
4. the safety hook blocks a mocked destructive payload:

```bash
printf '%s' '{"tool_args":{"CommandLine":"rm -rf /"}}' \
  | node .agents/hooks/validate-tool-call.mjs
```

Do not execute a real destructive command to test the hook.

## MCP migration

The repository's `.agents/mcp_config.json` remains the workspace source. It contains an example placeholder and is not automatically copied into the home directory.

Review first:

```bash
node .agents/hooks/sync-mcp.mjs --check
node .agents/hooks/sync-mcp.mjs --print
```

After replacing placeholders, explicitly apply to one target:

```bash
node .agents/hooks/sync-mcp.mjs --apply --target suite
node .agents/hooks/sync-mcp.mjs --apply --target cli
```

Rules:

- unresolved placeholders block `--apply`;
- existing server names are preserved unless `--force` is supplied;
- an existing target file is backed up before writing;
- credentials must remain outside version control.

## Safety hook compatibility

The hook fails open when Antigravity sends invalid JSON or an unrecognized command payload. This avoids locking the entire workspace after an upstream payload change. Valid, recognized destructive commands fail closed with a non-zero exit code.

To temporarily disable only the AG Kit hook:

```json
{
  "enabled": false
}
```

Keep Antigravity's native permission and workspace-trust controls enabled. Report payload compatibility issues privately when logs may contain prompts, paths, command arguments, or secrets.

## Plugin migration

Plugin installation is optional. Build and inspect it first:

```bash
npm run build:antigravity-plugin
agy plugin install ./dist/antigravity-plugin
agy plugin list
```

The repository-native `.agents/` directory remains the project source of truth. Avoid simultaneously editing generated plugin content and source `.agents` files.

## Rollback

To restore the pre-upgrade toolkit backup:

```bash
ag-kit rollback
```

After rollback, reopen Antigravity so it reloads the previous workspace configuration. If a global MCP file was explicitly synchronized, restore its timestamped `.ag-kit-backup-*` file separately.

## Compatibility summary

| Area | Migration impact |
| --- | --- |
| Agent, skill, workflow names | No breaking rename |
| Memory schema | No breaking change |
| CLI init/update/rollback | Existing merge-aware behavior retained |
| Antigravity hook | New and enabled by default |
| MCP home-directory config | Never changed automatically |
| Plugin | Optional new packaging path |
| Other AI runtimes | Markdown may remain usable, but no production runtime guarantee |
