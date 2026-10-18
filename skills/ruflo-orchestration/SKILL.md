---
name: ruflo-orchestration
description: Coordinate substantial software work with the local Ruflo MCP server and Muse Code. Use when the user asks for a swarm, persistent task memory, a multi-step workflow, Ruflo tools, or a clean-room feature-parity plan.
metadata:
  short-description: Plan and coordinate substantial work with local Ruflo tools
argument-hint: "<goal>"
---

# Muse + Ruflo orchestration

Use this skill for work that benefits from durable task state, a written decomposition, parallel investigation, or verification. Do not add orchestration overhead to a one-file or one-turn change.

## Safety and runtime boundary

- Treat Muse Code as the only model runtime in this integration. Its authenticated session is managed by Muse Code; do not ask the user for, create, print, store, or try to work around `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, or another provider key.
- Ruflo's local MCP process provides orchestration, task state, memory, routing metadata, and supported local tools. It does not turn a missing model provider into a model. If a Ruflo capability explicitly requires a separate cloud provider, OAuth grant, paid connector, or third-party secret, identify it as unavailable rather than bypassing authentication.
- Respect normal Muse Code approvals. Never loosen sandboxing, trust a workspace, enable a plugin, or approve a tool on the user's behalf.
- For a product-replica request, reproduce only functionality the user is entitled to implement. Do not copy proprietary code, private APIs, credentials, copyrighted copy or assets, trademarks, data behind a login, or paywalled material.

## First checks

1. Confirm that the current workspace is trusted before relying on its `.mcp.json`.
2. Use `/mcp` or the MCP inventory to confirm that the `ruflo` server is live. If it is unavailable, explain the actual startup/configuration error and continue with Muse Code's built-in tools where appropriate.
3. Read the repository's existing instructions and tests before creating a plan.
4. For complex work, write a compact task graph: goal, constraints, deliverables, dependencies, owner/agent role, test evidence, and rollback point.

## Execution pattern

1. **Scope** — restate the desired outcome and list assumptions that need confirmation.
2. **Decompose** — split independent investigation, implementation, testing, and review into bounded tasks. Prefer no more parallel tasks than the task can safely merge.
3. **Remember** — persist only durable, non-secret facts: decisions, interfaces, constraints, tests, and unresolved risks. Never persist passwords, tokens, private user data, or source code from an unauthorized system.
4. **Implement** — make small, reviewable changes. Keep task ownership clear and avoid overlapping edits to the same files.
5. **Verify** — run the relevant tests, linters, builds, or smoke checks. Record the result and any skipped check with a reason.
6. **Report** — summarize completed work, files changed, evidence, remaining risks, and the next decision needed.

## Ruflo tool discipline

When the local MCP server exposes equivalent tools, use the smallest suitable capability:

- memory tools for durable project facts and retrieval;
- task/workflow tools for explicit task status and handoffs;
- swarm/agent planning tools only when parallel roles materially improve the outcome;
- security or code-analysis tools before high-risk changes, never as a substitute for testing.

Tool names and availability differ by Ruflo release. Discover the live tool inventory instead of inventing tool names or claiming that every upstream plugin is installed.

## Clean-room parity work

When asked to make a compatible alternative:

1. Build a public, evidence-linked feature map first.
2. Separate functional behavior from brand, content, datasets, private integrations, and network effects.
3. Implement new code, copy, design tokens, and assets. Give the result its own name and visual identity.
4. Keep a feature matrix with `must`, `should`, `could`, intentionally omitted, implementation status, and test evidence.
5. State a measured compatibility result; never claim 100% parity without reproducible end-to-end evidence for every in-scope feature.
