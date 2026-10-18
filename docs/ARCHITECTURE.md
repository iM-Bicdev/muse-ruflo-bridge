# Architecture

## Goal

Connect an authenticated Muse Code session to Ruflo's local MCP process without
injecting third-party model-provider credentials into a repository, shell
profile, plugin, or MCP configuration.

## Components

```text
User
  │
  ▼
Muse Code session ── official Meta sign-in / plan ──► Muse model runtime
  │
  ├─ loads Muse ↔ Ruflo Bridge content plugin
  │    └─ skill + prompt commands only; no hook and no executable plugin MCP
  │
  └─ reads trusted project .mcp.json
       └─ starts: npx --yes ruflo@<exact-version> --no-update mcp start
            └─ local stdio MCP tools: memory, tasks, workflows, supported plugins
```

## Why project `.mcp.json` instead of a plugin-owned server

Muse Code plugins can ship MCP servers, but plugin MCP capability definitions
have no `env`, `cwd`, timeout or user credential fields and need a separate
runtime approval. A project `.mcp.json` is the documented fit for a local tool
that belongs to one repository. It also makes the executable command visible in
version control and requires workspace trust before Muse Code reads it.

The content plugin is intentionally separate: it tells the model when and how
to use the live tool inventory, without auto-starting tools or asserting a
capability that does not exist in the installed Ruflo release.

## Keyless means provider-keyless

This bridge is keyless only in the following precise sense:

- it does not need an Anthropic, OpenAI, Google, OpenRouter, or Ruflo provider
  key in order to attach Ruflo's local MCP process to Muse Code;
- Muse Code is already authenticated through Meta's official login flow;
- the local MCP child receives no configured provider secret from this bridge.

It does **not** mean bypassing an account, subscription, OAuth consent, paid
service, model quota, or a provider's authorization requirement. Those remain
owned by their respective providers.

## Lifecycle

1. `install.sh` validates the content package and installs it at user or project
   scope.
2. `scripts/merge_mcp.py` atomically adds an exact pinned `ruflo` server entry,
   or refuses to overwrite a different entry.
3. On a new session in a trusted workspace, Muse Code starts the stdio MCP
   server and discovers its actual tools.
4. The skill uses only tools present in that live inventory.
5. `uninstall.sh` removes the MCP entry only when it still exactly matches the
   managed definition, preventing accidental deletion of user configuration.

## Feature parity

Ruflo changes rapidly and exposed MCP tools vary by version, platform and
optional dependency. `100% compatibility` is therefore a test result, not a
marketing property. A release should map each in-scope upstream command/tool
against a reproducible Muse Code + Bridge test and publish unsupported items
explicitly.
