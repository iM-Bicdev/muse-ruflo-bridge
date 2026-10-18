#!/usr/bin/env python3
"""Add, inspect, or remove this integration's exact Muse Code MCP entry.

The script deliberately refuses to overwrite a differently configured `ruflo`
entry. That keeps an existing user-managed MCP server configuration intact.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

VERSION_RE = re.compile(r"^[0-9][0-9A-Za-z.+-]*$")


def desired_entry(version: str) -> dict[str, Any]:
    if not VERSION_RE.fullmatch(version):
        raise ValueError("Ruflo version must be a pinned, npm-safe version string")
    # An exact Ruflo release prevents a future `latest` release from silently
    # changing the local MCP process that Muse Code starts.
    return {
        "type": "stdio",
        "command": "npx",
        "args": ["--yes", f"ruflo@{version}", "--no-update", "mcp", "start"],
        "required": False,
        "startup_timeout_sec": 90,
        "tool_timeout_sec": 300,
    }


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"mcpServers": {}}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    if "mcpServers" not in value:
        value["mcpServers"] = {}
    if not isinstance(value["mcpServers"], dict):
        raise ValueError(f"{path}.mcpServers must be a JSON object")
    return value


def is_exact_entry(value: Any, expected: dict[str, Any]) -> bool:
    return value == expected


def save_config(path: Path, config: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(config, ensure_ascii=False, indent=2) + "\n"
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(rendered, encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".", help="Muse Code project directory (default: current directory)")
    parser.add_argument("--version", default="3.56.10", help="Exact Ruflo npm version to use")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="Check only; do not write")
    action.add_argument("--remove", action="store_true", help="Remove only this script's exact entry")
    args = parser.parse_args()

    try:
        expected = desired_entry(args.version)
        project = Path(args.project).expanduser().resolve()
        if not project.is_dir():
            raise ValueError(f"Project directory does not exist: {project}")
        path = project / ".mcp.json"
        config = load_config(path)
        servers = config["mcpServers"]
        current = servers.get("ruflo")

        if args.check:
            if is_exact_entry(current, expected):
                print(f"ok\t{path}\truflo@{args.version}")
                return 0
            if current is None:
                print(f"missing\t{path}\truflo entry is not installed", file=sys.stderr)
            else:
                print(f"different\t{path}\truflo exists but is not managed by this bridge", file=sys.stderr)
            return 1

        if args.remove:
            if current is None:
                print(f"unchanged\t{path}\truflo entry was absent")
                return 0
            if not is_exact_entry(current, expected):
                raise ValueError(
                    "Refusing to remove ruflo: the current entry differs from this bridge's exact pinned entry"
                )
            del servers["ruflo"]
            save_config(path, config)
            print(f"removed\t{path}\truflo@{args.version}")
            return 0

        if current is not None and not is_exact_entry(current, expected):
            raise ValueError(
                "Refusing to overwrite existing mcpServers.ruflo. Review it manually or use a different server name."
            )
        if current is None:
            servers["ruflo"] = expected
            save_config(path, config)
            print(f"installed\t{path}\truflo@{args.version}")
        else:
            print(f"unchanged\t{path}\truflo@{args.version}")
        return 0
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
