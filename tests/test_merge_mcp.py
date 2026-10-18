from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "merge_mcp.py"
VERSION = "3.56.10"
EXPECTED = {
    "type": "stdio",
    "command": "npx",
    "args": ["--yes", f"ruflo@{VERSION}", "--no-update", "mcp", "start"],
    "required": False,
    "startup_timeout_sec": 90,
    "tool_timeout_sec": 300,
}


class MergeMcpTests(unittest.TestCase):
    def run_script(self, project: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--project", str(project), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_installs_exact_entry_and_keeps_other_servers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            original = {"$schema": "https://example.invalid/schema", "mcpServers": {"docs": {"url": "https://example.invalid/mcp"}}}
            (project / ".mcp.json").write_text(json.dumps(original), encoding="utf-8")

            result = self.run_script(project)
            self.assertEqual(result.returncode, 0, result.stderr)
            config = json.loads((project / ".mcp.json").read_text(encoding="utf-8"))
            self.assertEqual(config["$schema"], original["$schema"])
            self.assertEqual(config["mcpServers"]["docs"], original["mcpServers"]["docs"])
            self.assertEqual(config["mcpServers"]["ruflo"], EXPECTED)

            checked = self.run_script(project, "--check")
            self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_refuses_to_overwrite_different_ruflo_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            before = {"mcpServers": {"ruflo": {"command": "something-else", "args": []}}}
            path = project / ".mcp.json"
            path.write_text(json.dumps(before), encoding="utf-8")

            result = self.run_script(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing to overwrite", result.stderr)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), before)

    def test_remove_only_managed_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(self.run_script(project).returncode, 0)
            result = self.run_script(project, "--remove")
            self.assertEqual(result.returncode, 0, result.stderr)
            config = json.loads((project / ".mcp.json").read_text(encoding="utf-8"))
            self.assertNotIn("ruflo", config["mcpServers"])

    def test_rejects_invalid_json_without_rewriting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            path = project / ".mcp.json"
            path.write_text("{ broken", encoding="utf-8")
            result = self.run_script(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not valid JSON", result.stderr)
            self.assertEqual(path.read_text(encoding="utf-8"), "{ broken")


if __name__ == "__main__":
    unittest.main()
