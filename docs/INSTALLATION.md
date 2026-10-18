# Installation and operations

## Prerequisites

Before installing the bridge, confirm that the target host has:

```bash
muse --version
node --version
npm --version
npx --version
python3 --version
git --version
```

Muse Code must be installed and authenticated through Meta's documented sign-in flow. Ruflo requires Node.js 20 or newer. The installer checks these prerequisites and stops before modifying the project when one is missing.

## Standard installation

Run from the root of the project that Muse Code will open:

```bash
git clone https://github.com/iM-Bicdev/muse-ruflo-bridge.git .muse-ruflo-bridge && bash .muse-ruflo-bridge/install.sh
```

The command performs the following actions:

1. Validates the native Muse Code plugin. Validation parses package metadata and does not execute plugin code.
2. Installs the Bridge content plugin at user scope by default.
3. Adds the pinned `mcpServers.ruflo` entry to the selected project's `.mcp.json`.
4. Re-checks the entry it wrote.

It does not start Ruflo, modify model-provider environment variables, or auto-approve executable plugin capabilities.

## Installer options

```text
bash install.sh [options]

  --project PATH        Target Muse Code project; default: current directory
  --scope user|project  Plugin scope; default: user
  --version VERSION     Exact Ruflo npm version; default: 3.56.10
  --skip-plugin         Add only the project MCP entry
  -h, --help            Show help
```

Examples:

```bash
# Install against a project without changing the current directory
bash .muse-ruflo-bridge/install.sh --project ~/code/service-a

# Install plugin content only for the selected project
bash .muse-ruflo-bridge/install.sh --scope project

# Review and deliberately pin a different upstream release
bash .muse-ruflo-bridge/install.sh --version 3.56.10
```

## First session

After installation:

1. Read `.mcp.json` and verify the exact command and Ruflo version.
2. Start a **new** Muse Code session inside the target project.
3. Respond to the workspace trust prompt only if you trust the repository and its configuration.
4. Enter `/mcp` and inspect the `ruflo` server result.
5. Run `/muse-ruflo-bridge:ruflo-health` for a read-only status report.

Muse Code starts project MCP servers on session start. An already-running session will not acquire the newly installed server; start a new session.

## Expected project configuration

The bridge only manages this exact entry:

```json
{
  "mcpServers": {
    "ruflo": {
      "type": "stdio",
      "command": "npx",
      "args": ["--yes", "ruflo@3.56.10", "--no-update", "mcp", "start"],
      "required": false,
      "startup_timeout_sec": 90,
      "tool_timeout_sec": 300
    }
  }
}
```

Existing `.mcp.json` properties and other servers are preserved. If an existing `ruflo` entry differs, installation fails rather than replacing it.

## Verify without starting Ruflo

```bash
python3 .muse-ruflo-bridge/scripts/merge_mcp.py --project . --check
```

A successful check proves that the exact expected configuration is present. It does not prove that the npm package can start or that a specific Ruflo tool is available; use `/mcp` in a new Muse Code session for runtime status.

## Upgrade policy

The default Ruflo release is intentionally pinned. To upgrade:

1. Read the upstream Ruflo release notes and security advisories.
2. Review the changed package version and its compatibility with Muse Code.
3. Update using an explicit version.
4. Start a new session and verify `/mcp` plus the relevant workflow tests.

Do not replace the configuration with `ruflo@latest` in a production or shared workspace unless you accept that unreviewed upstream changes may alter the executable MCP server.

## Uninstall

```bash
bash .muse-ruflo-bridge/uninstall.sh --project .
```

The uninstaller removes the content plugin and deletes the `ruflo` entry only when it exactly matches the bridge-managed configuration. If you later edited the entry, it refuses to delete it. Use `--keep-plugin` to remove only the project MCP configuration.

## Troubleshooting

| Symptom | Likely cause | Resolution |
|---|---|---|
| `Missing required command: muse` | Muse Code is not installed or not on `PATH`. | Install Muse Code from Meta's official documentation, sign in, then rerun the installer. |
| `Ruflo requires Node.js 20 or newer` | Unsupported Node.js runtime. | Upgrade Node.js and rerun the installer. |
| Installer refuses to overwrite `mcpServers.ruflo` | A user-managed Ruflo configuration already exists. | Review the existing entry; keep it, rename it manually, or align it with the intended pin. |
| Ruflo is absent from `/mcp` | The session started before installation, workspace is untrusted, or the server failed to start. | Start a new trusted session and inspect `/mcp` diagnostics. |
| Ruflo MCP startup times out | First-run npm/optional dependency initialization can be slow. | Confirm network access, use the pinned version, inspect Ruflo logs/diagnostics, and retry in a new session. |
| A cloud-specific Ruflo feature asks for credentials | The feature is outside the keyless local bridge scope. | Use the provider's official documented authentication path; do not add secrets to this repository. |
