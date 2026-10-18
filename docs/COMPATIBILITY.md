# Compatibility and verification status

## Purpose

Muse ↔ Ruflo Bridge is an **integration**, not a fork or reimplementation of Ruflo. The project configures Muse Code to start an exact upstream Ruflo MCP release and supplies a Muse-native workflow skill. It therefore has two different kinds of compatibility:

1. **Bridge compatibility** — whether this repository safely installs and configures the integration.
2. **Upstream runtime availability** — which Ruflo tools and optional capabilities the pinned upstream release exposes on a particular host.

Those must not be conflated with “full Ruflo parity.”

## Current measured status

| Area | Status | Evidence |
|---|---|---|
| Native Muse plugin manifest shape | Static validation ready | JSON manifest and referenced files are present; run `muse plugins validate .` on a Muse Code host. |
| Safe `.mcp.json` creation | Verified | Automated tests cover creation, preservation of other servers, idempotency, and invalid JSON refusal. |
| Safe `.mcp.json` removal | Verified | Automated test confirms only the exact bridge-managed entry is removed. |
| Local Ruflo stdio command registration | Verified as configuration | The command is pinned and documented; runtime start must be tested on the destination Muse Code host. |
| Live Muse ↔ Ruflo MCP handshake | Not yet measured in CI | Requires a Muse Code binary, trust decision, Node 20+, npm access, and a live session. |
| Ruflo tool inventory | Host-dependent | Discover via `/mcp` after startup; no tool names are assumed by the Bridge. |
| Ruflo cloud/provider integrations | Out of scope by default | They require their own official provider credentials and consent flows. |

## Similarity to Ruflo

### Source-code similarity: 0%

This repository contains no copied, vendored, or ported Ruflo source files. It starts the published upstream `ruflo` npm package at runtime and contains only its own shell, Python, JSON, Markdown, and test files. In that meaningful source-level sense, the project is **0% a Ruflo code clone**.

### Functional parity: intentionally not scored yet

A numeric “percent like Ruflo” would be misleading at this stage because the project does not reimplement Ruflo's commands, agents, plugins, memory engine, router, hooks, daemon, console, or cloud integrations. It provides:

- one Muse Code orchestration skill;
- three Muse Code prompt commands;
- a safe installation and removal flow;
- one configuration path that exposes the **actual capabilities of the pinned upstream Ruflo MCP server** when that server starts successfully.

In other words, the Bridge implements a narrow integration surface, while its runtime can expose upstream Ruflo tools rather than duplicate them. It is not appropriate to claim `100%`, or any other percentage, until a defined feature scope is exercised end-to-end.

## How to produce a defensible parity score

For a specific Ruflo release and a specific Muse Code version:

1. Freeze the Ruflo version and operating-system matrix.
2. Export the live upstream tool catalog from `/mcp`.
3. Build a feature matrix covering CLI commands, MCP tools, skills, agent types, plugin families, hooks, daemon behavior, memory backends, and integrations.
4. Mark each feature as supported, unsupported, intentionally out of scope, partially supported, or not applicable to Muse Code.
5. Add reproducible integration tests for every claimed supported feature.
6. Publish the weighted scope and results alongside the release.

Only that process can yield a meaningful percentage. Until then, the correct public status is: **safe integration scaffold; runtime parity unmeasured**.

## Scope boundaries

The following upstream capabilities need separate design, testing, and sometimes external authorization before they can be claimed:

- provider-specific model execution and failover;
- managed or cloud agents;
- OAuth-backed connectors and commercial data sources;
- browser automation against third-party services;
- remote/HTTP MCP exposure and federation;
- optional native or model dependencies;
- product-specific UI, console, daemon, and hook behavior.

The Bridge will not bypass any of those authorization or licensing boundaries.
