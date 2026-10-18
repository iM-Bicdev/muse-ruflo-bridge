# Muse ↔ Ruflo Bridge

[![Verify](https://github.com/iM-Bicdev/muse-ruflo-bridge/actions/workflows/verify.yml/badge.svg)](https://github.com/iM-Bicdev/muse-ruflo-bridge/actions/workflows/verify.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A conservative, project-local bridge that connects [Meta Muse Code](https://dev.meta.ai/docs/muse-code) to Ruflo's local MCP server. It adds a Muse-native skill package, a pinned Ruflo MCP registration, and safe installation/removal tooling—without writing third-party model-provider API keys into your project.

> **Status: pre-release.** The bridge is tested for configuration safety. End-to-end runtime validation requires a host with Muse Code, Node.js 20+, and access to the pinned Ruflo npm release.

## What this project is

Muse ↔ Ruflo Bridge treats **Muse Code as the authenticated model and agent host** and **Ruflo as a local orchestration and MCP capability layer**. The integration installs a small Muse Code content plugin and adds an optional `ruflo` stdio server to the current project's `.mcp.json`.

```text
Muse Code session
  ├─ authenticated through Meta's official sign-in flow
  ├─ loads the Bridge skill and prompt commands
  └─ starts trusted project MCP configuration
       └─ npx --yes ruflo@<pinned-version> --no-update mcp start
            └─ local memory, task, workflow, and supported Ruflo MCP tools
```

## What this project is not

- It is **not** a replacement model, a method to bypass authentication, or a way to evade model quotas or subscriptions.
- It does **not** request, create, export, or store `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, or other model-provider secrets.
- It is **not** a reimplementation or a source-level clone of Ruflo. Ruflo is integrated as its published MIT-licensed package.
- It does **not** guarantee every Ruflo plugin, cloud feature, provider integration, or optional dependency will be available in every Muse Code environment.

## Features

- **Muse-native content plugin** with one orchestration skill and three slash commands.
- **Pinned upstream runtime**: uses an explicit Ruflo version rather than `latest`.
- **Project-local MCP configuration**: no global mutation of Muse Code settings is required.
- **Conservative configuration merge**: refuses to overwrite a different `mcpServers.ruflo` entry.
- **Safe removal**: removes only the exact configuration entry installed by this bridge.
- **No runtime auto-approval**: the plugin declares no executable hooks, plugin MCP server, or reminders.
- **Clean-room planning guidance** for lawful feature-parity work using public and authorized sources only.

## Requirements

| Requirement | Version / notes |
|---|---|
| Muse Code | Installed and signed in through Meta's official flow |
| Node.js | 20 or later |
| npm and npx | Available on `PATH` |
| Python | Python 3 for the configuration utility |
| Git | Required for the one-line clone-and-install workflow |
| Network | Required on first MCP startup if the pinned npm package is not cached |

## Quick start

Run the following command from the root of the project you want to open with Muse Code:

```bash
git clone https://github.com/iM-Bicdev/muse-ruflo-bridge.git .muse-ruflo-bridge && bash .muse-ruflo-bridge/install.sh
```

The installer validates and installs the content plugin, then adds an exact `ruflo` MCP entry to the target project's `.mcp.json`. It **does not** start Ruflo during installation and does not write secrets.

Next:

1. Review the generated or updated `.mcp.json`.
2. Start a **new** Muse Code session from the target workspace.
3. Trust the workspace only after reviewing its contents.
4. Open `/mcp` and verify that the `ruflo` server is live.
5. Run `/muse-ruflo-bridge:ruflo-health` for a read-only integration review.

See [Installation](docs/INSTALLATION.md) for flags, scope choices, upgrades, and troubleshooting.

## Installed components

### Muse Code content plugin

| Capability | Invocation | Purpose |
|---|---|---|
| Skill | `ruflo-orchestration` | Guides bounded multi-step work, memory discipline, verification, and safe tool discovery. |
| Command | `/muse-ruflo-bridge:ruflo-health` | Produces a read-only integration status review. |
| Command | `/muse-ruflo-bridge:ruflo-swarm-plan <goal>` | Creates a decision-complete multi-agent execution plan without changing files. |
| Command | `/muse-ruflo-bridge:ruflo-replica-plan <target>` | Produces a lawful clean-room feature-parity plan from authorized evidence. |

### Project MCP entry

By default, the installer writes this exact entry under `mcpServers.ruflo`:

```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["--yes", "ruflo@3.56.10", "--no-update", "mcp", "start"],
  "required": false,
  "startup_timeout_sec": 90,
  "tool_timeout_sec": 300
}
```

The entry is optional by design: if Ruflo cannot start, Muse Code remains usable and `/mcp` reports the failure. The bridge never overwrites an existing, different Ruflo entry.

## Configuration and operations

### Validate the configuration

```bash
python3 .muse-ruflo-bridge/scripts/merge_mcp.py --project . --check
```

### Install against another project or pin another Ruflo release

```bash
bash .muse-ruflo-bridge/install.sh \
  --project /path/to/project \
  --version 3.56.10
```

Review release notes and source changes before changing the pinned version.

### Remove the bridge

```bash
bash .muse-ruflo-bridge/uninstall.sh --project .
```

Removal is deliberately conservative: it refuses to delete a `ruflo` configuration that differs from the exact entry installed by this project.

## Capability scope

The bridge is an integration layer, not a feature clone. The actual tools available to Muse Code are discovered from the live Ruflo MCP server at session startup and may vary by Ruflo release, operating system, optional dependencies, and the user's approved environment.

| Area | Bridge status | Notes |
|---|---|---|
| Muse Code session and model host | Supported | Uses official Muse Code authentication; no provider key is configured by this project. |
| Ruflo local stdio MCP registration | Supported | Pinned, optional, project-local configuration. |
| Ruflo tool discovery | Supported at session startup | Inspect `/mcp`; do not assume a tool exists until it is advertised. |
| Local orchestration, memory, and task workflows | Upstream-dependent | Available only when exposed by the pinned Ruflo server on the host. |
| Ruflo cloud providers, managed agents, OAuth connectors, commercial data | Out of scope by default | Require the provider's own documented authentication and consent flow. |
| Full Ruflo product parity | Not claimed | See [Compatibility](docs/COMPATIBILITY.md). |

## Security model

The most important decision is whether to trust the workspace. A project `.mcp.json` can start a local program, so inspect it before granting trust in Muse Code.

- The bridge uses a pinned npm package version, never `latest`.
- The MCP entry contains no `env` block and passes no secrets.
- The Muse plugin contains only skills and commands; it cannot execute hooks or start an MCP process on its own.
- Normal Muse Code approvals still govern tool calls.
- Do not expose the default local stdio MCP server as a network service without a separate authentication and threat-model review.

Read the complete [security model](docs/SECURITY.md) before deploying the bridge in a shared or production environment.

## Clean-room feature-parity work

The `ruflo-replica-plan` command follows a clean-room workflow inspired by the requested `replica-skill` project. Use it only with public material and accounts you are authorized to use. Do not copy proprietary source, private APIs, credentials, assets, trademarks, copyrighted copy, paywalled content, or another user's data.

Ruflo itself is MIT licensed, so the correct route for Ruflo-specific work is direct, attributed integration—not reverse engineering. See [Replica-skill note](docs/REPLICA-SKILL-NOTE.md).

## Development

```bash
# Run repository tests
python3 -m unittest discover -s tests -v

# Check shell syntax
bash -n install.sh
bash -n uninstall.sh

# Validate the plugin on a machine with Muse Code installed
muse plugins validate .
```

The automated test suite covers safe MCP configuration creation, idempotency, non-destructive behavior, removal, and invalid JSON handling. It intentionally does not start Ruflo or make a model-provider request.

## Documentation

- [Installation and operations](docs/INSTALLATION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Compatibility and verification status](docs/COMPATIBILITY.md)
- [Security model](docs/SECURITY.md)
- [Clean-room / replica-skill note](docs/REPLICA-SKILL-NOTE.md)
- [Attributions](ATTRIBUTIONS.md)
- [Changelog](CHANGELOG.md)

## License and attribution

This bridge is available under the [MIT License](LICENSE). It does not vendor upstream source. Ruflo and replica-skill retain their own MIT licenses and copyright notices; see [ATTRIBUTIONS.md](ATTRIBUTIONS.md).
