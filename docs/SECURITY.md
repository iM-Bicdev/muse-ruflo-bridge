# Security model

## Trust boundaries

| Boundary | Control |
|---|---|
| Muse model access | Official Meta login/session; this repository cannot and does not replace it. |
| Project code and `.mcp.json` | Muse Code workspace trust prompt. Review before granting trust. |
| Ruflo process | Local stdio child launched by Muse Code from a pinned npm version. |
| Actions performed by tools | Muse Code's normal approval policy. |
| Provider keys / OAuth credentials | Never written or passed by this bridge. Use the provider's official credential path if an optional feature needs one. |

## Design decisions

- **Exact package version.** The MCP entry uses `ruflo@3.56.10`, not `latest`.
  Updating requires an explicit review and `--version` choice.
- **No `env` block.** The project MCP configuration deliberately does not pass
  secrets to Ruflo. Muse Code also starts stdio children from a restricted
  environment.
- **No automatic runtime approval.** The Muse plugin only contains textual
  skills and commands. It declares no hooks, no MCP server and no reminder.
- **Conservative merge/removal.** The JSON utility refuses to overwrite or
  remove a non-identical existing `mcpServers.ruflo` entry.
- **No remote HTTP server.** The default is local stdio only. Do not expose a
  Ruflo MCP server to a network without an authenticated transport, access
  controls and a threat-model review.

## User review checklist

Before trusting the workspace:

1. Open `.mcp.json`; confirm that `command` is `npx` and the Ruflo version is
   the version you intended to run.
2. Read the pinned Ruflo release notes and source/license where appropriate.
3. Inspect `muse plugins inspect muse-ruflo-bridge` and the plugin's source.
4. Run `/mcp` in a new Muse Code session and confirm the server name and tools.
5. Keep normal tool approvals enabled for write, shell, browser and network
   actions.

## Reporting

Do not include secrets, access tokens, personal data or proprietary source in a
public issue. Describe the installed bridge release, Muse Code version, Node
version, platform, the redacted MCP error and reproducible steps.
