# Release setup

The workflow files provide a secure baseline, but maintainers must configure repository and environment settings before production use.

## Branch protection

Protect `main` and require pull requests. Require these checks before merge:

- `Toolkit validation`
- `CLI tests and package validation`
- `Web lint, typecheck, build, and audit`
- `Antigravity native contract`
- `dependency-review`

Dismiss stale approvals after new commits. Block force pushes and branch deletion. Keep release PRs in Draft until the hands-on Antigravity smoke test in `PRODUCTION_CHECKLIST.md` is complete and recorded in the PR.

## npm Trusted Publishing

1. In npm package settings for `@vudovn/ag-kit`, configure GitHub Actions as a trusted publisher.
2. Set the repository and workflow to `.github/workflows/publish.yml`.
3. Create a GitHub Environment named `npm` and require approval when appropriate.
4. Remove any legacy `NPM_TOKEN` secret after a successful OIDC release.

The publish workflow requires `id-token: write` and must not consume a long-lived npm token.

## Production deployment

Create a protected GitHub Environment named `production`. Store deployment values as environment secrets/variables using placeholders appropriate to the selected platform, for example:

- `DOKPLOY_TOKEN`
- `DOKPLOY_URL`
- `DOKPLOY_APPLICATION_ID`

Never place token samples, internal addresses, application IDs, or private certificate material in repository documentation.

Require an approval gate and a rollback plan before the deployment job can access production credentials.

## Antigravity release evidence

Before marking a release PR ready:

1. run the full automated command set in `PRODUCTION_CHECKLIST.md`;
2. open the release branch in a trusted Antigravity staging workspace;
3. verify rules, skills, workflows, `/agents`, `/tasks`, and approval checkpoints;
4. test the destructive-command policy with mocked stdin only;
5. configure a non-placeholder staging MCP server and verify discovery;
6. build, inspect, install, and list the local plugin bundle;
7. record Antigravity build/channel, operating system, results, and unresolved warnings in the PR.

## GitHub security settings

Enable:

- private vulnerability reporting;
- Dependabot alerts, security updates, and version updates;
- dependency graph and Dependency Review;
- secret scanning and push protection when available;
- CodeQL default setup for JavaScript/TypeScript and Python;
- protected `npm` and `production` environments;
- branch rules that prevent required checks from being bypassed.

## Release operator checklist

The release operator must confirm:

- root, CLI, web, lock files, `.agents/VERSION`, manifest, and web changelog use the same version;
- the Git tag matches the package version exactly;
- generated `.agents` registry, integrity lock, dependency graph, and plugin inventory are current;
- release notes match `CHANGELOG.md`;
- no package, release, or deployment action starts before the PR is approved and merged;
- rollback commands and prior artifacts are available.
