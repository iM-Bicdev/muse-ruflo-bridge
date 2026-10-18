# Contributing

Thank you for improving Muse ↔ Ruflo Bridge.

## Principles

- Keep installation non-destructive and easy to audit.
- Never add provider credentials, tokens, or personal data to the repository, examples, tests, or logs.
- Pin executable upstream dependencies; do not replace pins with `latest` without an explicit release policy.
- Do not claim support for a Ruflo capability until it has an evidence-backed compatibility test.
- Preserve the boundary between local, keyless Muse Code integration and features that require separate provider authentication.

## Local checks

Run the following before opening a pull request:

```bash
python3 -m unittest discover -s tests -v
python3 -m json.tool .muse-plugin/plugin.json >/dev/null
bash -n install.sh
bash -n uninstall.sh
```

On a machine with Muse Code installed, also run:

```bash
muse plugins validate .
```

For any change to `scripts/merge_mcp.py`, add or update a test that proves the change is safe around an existing `.mcp.json`.

## Pull requests

1. Explain the user-visible behavior and the security impact.
2. Keep unrelated formatting changes out of the same pull request.
3. State the Muse Code version, Ruflo version, operating system, and commands used for any runtime validation.
4. Update `README.md`, `docs/COMPATIBILITY.md`, and `CHANGELOG.md` when the supported surface changes.
5. Do not include a credential, private URL, screenshot containing secrets, or output from an unauthorized target.

## Reporting security issues

Do not open a public issue containing a token or exploit details that could put users at risk. Follow the guidance in [SECURITY.md](SECURITY.md).
