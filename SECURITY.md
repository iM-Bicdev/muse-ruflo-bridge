# Security policy

Muse ↔ Ruflo Bridge starts a local executable MCP process from a trusted Muse Code workspace. Please read the full [security model](docs/SECURITY.md) before installation or deployment.

## Reporting a vulnerability

Do not publish secrets, access tokens, private source code, or exploit details in a public issue. Open a private GitHub security advisory for this repository when available, or contact the repository owner through a private channel with:

- a clear reproduction path;
- affected bridge version and commit;
- Muse Code, Ruflo, Node.js, and operating-system versions;
- the smallest redacted proof of impact;
- suggested mitigation, if known.

Please allow time for assessment and remediation before public disclosure.

## Supported security posture

The bridge is designed to:

- pin the Ruflo npm package version;
- avoid provider API keys and secret environment variables;
- require normal Muse Code workspace trust and tool approvals;
- preserve existing, non-matching Ruflo MCP configuration rather than overwrite it;
- avoid exposing an unauthenticated network MCP server by default.
