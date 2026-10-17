# Security policy

## Supported versions

AG Kit uses calendar versioning. Security fixes are provided for the latest published release. Upgrade the CLI and toolkit before reporting an issue already fixed in a newer release.

## Reporting a vulnerability

Use GitHub private vulnerability reporting or the repository Security Advisory flow. Do not publish suspected secrets, exploitable command payloads, private paths, prompt contents, source code, or proof-of-concept data in a public issue.

Include only sanitized information:

- affected AG Kit, CLI, web, and `.agents` versions;
- Antigravity build/channel and operating system;
- Node.js and Python versions;
- affected hook, MCP server, plugin file, agent, skill, workflow, CLI command, CI job, or deployment path;
- minimal reproduction steps with credentials and private data removed;
- expected impact, observed behavior, and known mitigations.

## Runtime threat model

The Antigravity integration assumes prompts, repository content, tool arguments, MCP responses, and third-party dependencies may be untrusted.

Primary risks:

- prompt or repository instructions inducing unsafe tool use;
- destructive shell commands reaching a trusted host;
- secrets embedded in MCP configuration or logs;
- malicious or compromised MCP servers;
- plugin artifact tampering or stale generated content;
- local/global configuration conflict during synchronization;
- upstream hook-payload changes causing false blocks or workspace lockout;
- dependency or GitHub Actions supply-chain compromise.

AG Kit reduces these risks but is not a sandbox. Keep Antigravity permissions, workspace trust, operating-system isolation, least-privilege credentials, code review, and human approval enabled.

## Native hook security boundary

`.agents/hooks.json` registers a `PreToolUse` hook for `run_command`. The policy reads at most 1 MiB of JSON from stdin, performs no network request, and blocks only high-confidence patterns:

- recursive deletion of a Unix filesystem root;
- filesystem formatting commands;
- raw-disk overwrite with `dd`;
- Windows drive formatting;
- recursive forced deletion of a Windows drive root.

Normal project cleanup such as deleting `dist/` or `node_modules/` is intentionally allowed.

Recognized destructive commands fail closed with a non-zero exit code. Invalid JSON, oversized input, or an unrecognized payload shape fails open with a warning to avoid an upstream schema change locking every tool call. Treat such warnings as compatibility incidents and investigate before production use.

To temporarily disable only the AG Kit hook, set `"enabled": false` in `.agents/hooks.json` and reopen the workspace. Do not disable Antigravity's own permission controls. Report false positives and payload-shape changes privately when data may be sensitive.

## MCP security boundary

`.agents/mcp_config.json` is an example workspace source and must not contain real credentials in version control.

`sync-mcp.mjs`:

- defaults to check-only behavior;
- refuses `--apply` while placeholders remain;
- preserves same-name existing servers unless `--force` is explicitly supplied;
- creates a timestamped backup before replacing an existing target file;
- writes only to the selected Antigravity suite or CLI target.

Review MCP server source, requested permissions, network destinations, and data-retention policy before enabling it. Prefer environment-based secret injection where supported. Rotate any credential that appears in a commit, log, artifact, issue, or chat transcript.

## Plugin and artifact security

The plugin builder reads repository files only. It does not copy environment variables or home-directory configuration. Review the generated `dist/antigravity-plugin/` directory and `PLUGIN_CONTENTS.json` before installation.

Do not install an artifact when:

- its version differs from `.agents/VERSION`;
- the content inventory is missing or unexpected;
- it contains a real MCP credential;
- it was generated from an unreviewed branch;
- required CI or Dependency Review checks failed.

## Update and rollback safety

`ag-kit update` uses a managed-file manifest and merge strategy by default. Local modifications are not silently overwritten. Conflicts produce an incoming copy and JSON report, while pre-update backups support `ag-kit rollback`.

Global MCP synchronization has a separate timestamped backup and must be restored separately when rolling back the toolkit.

## Repository and release baseline

The repository expects:

- immutable commit-SHA references for GitHub Actions;
- least-privilege `GITHUB_TOKEN` permissions;
- protected `main`, `production`, and `npm` environments;
- npm Trusted Publishing through OIDC instead of a long-lived npm token;
- private vulnerability reporting, Dependabot, secret scanning, and push protection where available;
- Toolkit validation, Antigravity native contract, CLI tests, web checks, Dependency Review, and production dependency audits before release;
- hands-on Antigravity smoke testing before a release PR leaves Draft.

See [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) and [.github/RELEASE_SETUP.md](.github/RELEASE_SETUP.md).
