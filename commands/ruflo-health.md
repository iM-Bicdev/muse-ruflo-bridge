---
description: Inspect the Muse ↔ Ruflo integration without adding credentials
argument-hint: "[detail]"
---

Perform a read-only health review of the Muse ↔ Ruflo integration for this workspace.

1. Check whether the workspace is trusted and whether `.mcp.json` contains a `ruflo` server.
2. Inspect the live MCP inventory. Do not invent a server or tool that is not present.
3. Check Node and npm versions only if terminal access is available; Ruflo requires Node 20 or newer.
4. Do not set, request, expose, or validate third-party provider API keys. The intended inference runtime is the current authenticated Muse Code session.
5. Return a compact status table with: skill installed, project MCP entry, MCP server state, local prerequisites, available local capabilities, unavailable capabilities, and the smallest safe fix.

Extra request: $ARGUMENTS
