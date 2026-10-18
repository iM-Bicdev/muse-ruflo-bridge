---
description: Create a bounded Ruflo/Muse multi-agent plan before implementation
argument-hint: "<goal>"
---

Create a decision-complete, bounded plan for this goal:

$ARGUMENTS

Before changing files:

- inspect the repository and relevant tests;
- state assumptions and ask only for decisions that block implementation;
- separate independent work from serial work;
- assign concise roles for discovery, implementation, test, and review only when the work benefits from parallelism;
- include data boundaries, security/privacy risks, merge order, test evidence, rollback, and acceptance criteria;
- specify which durable non-secret facts should be stored in Ruflo memory if the live MCP inventory provides that capability.

Do not start agents, edit files, approve tools, or claim task completion in this response. Stop after the plan.
