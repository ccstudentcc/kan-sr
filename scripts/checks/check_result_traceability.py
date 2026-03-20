"""Check traceability of key conclusion documents.

This check enforces that conclusion docs contain:
1) Traceable output artifact paths (for example `output/...`).
2) Reproducible command lines (for example `python scripts/...`).
3) Executable command references (script exists and supports `--help`).
4) Referenced CLI flags are present in script help text.
"""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


OUTPUT_PATH_RE = re.compile(r"\boutput(?:/[^\s`]*)?")
COMMAND_RE = re.compile(r"\bpython[ \t]+scripts/[A-Za-z0-9._/-]+\.py(?:[ \t]+[^\n`]*)?")
FLAG_RE = re.compile(r"--[a-zA-Z0-9][a-zA-Z0-9-]*")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate that conclusion docs provide artifact paths and valid commands."
    )
    parser.add_argument(
        "--docs",
        nargs="+",
        default=["CURRENT_WORK_REFERENCE.md"],
        help="Markdown documents to validate.",
    )
    return parser.parse_args()


def extract_script_path(command: str) -> str:
    """Extract script path from command string."""
    tokens = shlex.split(command, posix=True)
    if len(tokens) < 2:
        return ""
    return tokens[1]


def extract_flags(command: str) -> List[str]:
    """Extract long-option flags from a command string."""
    return FLAG_RE.findall(command)


def collect_help_cache(commands: List[str]) -> Dict[str, str]:
    """Run `--help` once per script and return help text cache."""
    cache: Dict[str, str] = {}
    for command in commands:
        script = extract_script_path(command)
        if not script:
            continue
        if script in cache:
            continue

        script_path = Path(script)
        if not script_path.exists():
            cache[script] = ""
            continue

        result = subprocess.run(
            [sys.executable, script, "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            cache[script] = ""
            continue
        cache[script] = f"{result.stdout}\n{result.stderr}"
    return cache


def main() -> int:
    """Run traceability checks and return process exit code."""
    args = parse_args()
    errors: List[str] = []

    doc_commands: Dict[Path, List[str]] = {}
    for doc in args.docs:
        path = Path(doc)
        if not path.exists() or not path.is_file():
            errors.append(f"Document not found: {path}")
            continue

        text = path.read_text(encoding="utf-8")
        path_matches = OUTPUT_PATH_RE.findall(text)
        cmd_matches = COMMAND_RE.findall(text)
        doc_commands[path] = cmd_matches

        if not path_matches:
            errors.append(
                f"{path}: missing traceable output artifact path (expected pattern like output/...)"
            )
        if not cmd_matches:
            errors.append(
                f"{path}: missing reproducible command (expected pattern like python scripts/...)"
            )

    all_commands = [cmd for commands in doc_commands.values() for cmd in commands]
    help_cache = collect_help_cache(all_commands)

    for doc_path, commands in doc_commands.items():
        for command in commands:
            script = extract_script_path(command)
            if not script:
                errors.append(f"{doc_path}: cannot parse command: {command}")
                continue

            script_path = Path(script)
            if not script_path.exists():
                errors.append(f"{doc_path}: script does not exist: {script}")
                continue

            help_text = help_cache.get(script, "")
            if not help_text:
                errors.append(
                    f"{doc_path}: script help check failed (not executable with --help): {script}"
                )
                continue

            for flag in extract_flags(command):
                if flag not in help_text:
                    errors.append(
                        f"{doc_path}: command references unknown flag '{flag}' for {script}"
                    )

    if errors:
        print("[ERROR] Result traceability check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[OK] Result traceability check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
