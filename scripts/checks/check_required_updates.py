"""Check required documentation updates based on changed files.

Rules:
- If execution scripts change (`scripts/run_*.py`, `scripts/summarize_*.py`),
  then both `EXPERIMENT_PROTOCOL.md` and `CURRENT_WORK_REFERENCE.md` must be updated.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class UpdateRule:
    """Define one change-triggered required update rule."""

    name: str
    trigger_globs: List[str]
    required_files: List[str]


RULES: List[UpdateRule] = [
    UpdateRule(
        name="execution scripts -> protocol and status docs",
        trigger_globs=[
            "scripts/run_*.py",
            "scripts/summarize_*.py",
            "scripts/experiment/*.py",
        ],
        required_files=["EXPERIMENT_PROTOCOL.md", "CURRENT_WORK_REFERENCE.md"],
    ),
]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate required doc updates when specific files are changed."
    )
    parser.add_argument(
        "--diff-ref",
        default="HEAD",
        help="Git ref for working-tree diff mode (uses `git diff --name-only <diff-ref>`).",
    )
    parser.add_argument(
        "--base-ref",
        default=None,
        help="Optional git base reference for range mode.",
    )
    parser.add_argument(
        "--head-ref",
        default=None,
        help="Optional git head reference for range mode.",
    )
    parser.add_argument(
        "--changed-files-file",
        type=Path,
        default=None,
        help="Optional text file containing one changed file path per line.",
    )
    parser.add_argument(
        "--strict-no-empty",
        action="store_true",
        help="Fail when changed files resolve to empty.",
    )
    return parser.parse_args()


def normalize(path_str: str) -> str:
    """Normalize path into POSIX-like relative style."""
    return path_str.strip().replace("\\", "/")


def load_changed_files_from_file(path: Path) -> List[str]:
    """Load changed files from plain text file."""
    if not path.exists():
        raise FileNotFoundError(f"Changed files list not found: {path}")
    lines = path.read_text(encoding="utf-8").splitlines()
    return [normalize(line) for line in lines if line.strip()]


def run_git_diff_name_only(diff_arg: str) -> List[str]:
    """Run git diff --name-only with a single diff target argument."""
    command = ["git", "diff", "--name-only", diff_arg]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown git diff error"
        raise RuntimeError(f"Failed to load changed files from git: {stderr}")
    return [normalize(line) for line in result.stdout.splitlines() if line.strip()]


def load_changed_files_from_git(
    diff_ref: str, base_ref: str | None, head_ref: str | None
) -> List[str]:
    """Load changed files from git using range mode or working-tree mode."""
    if base_ref and head_ref:
        return run_git_diff_name_only(f"{base_ref}..{head_ref}")
    if base_ref or head_ref:
        raise RuntimeError("Both --base-ref and --head-ref must be provided together.")
    return run_git_diff_name_only(diff_ref)


def any_match(paths: Iterable[str], globs: Iterable[str]) -> bool:
    """Return True if any path matches any provided glob."""
    return any(fnmatch.fnmatch(path, pattern) for path in paths for pattern in globs)


def find_missing_required_files(changed_files: List[str], required_files: List[str]) -> List[str]:
    """Return required files not present in changed file list."""
    changed_set = set(changed_files)
    return [req for req in required_files if normalize(req) not in changed_set]


def main() -> int:
    """Run required-update checks and return process exit code."""
    args = parse_args()

    try:
        if args.changed_files_file is not None:
            changed_files = load_changed_files_from_file(args.changed_files_file)
        else:
            changed_files = load_changed_files_from_git(
                diff_ref=args.diff_ref,
                base_ref=args.base_ref,
                head_ref=args.head_ref,
            )
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"[ERROR] {exc}")
        return 1

    is_ci = str(os.getenv("CI", "")).strip().lower() in {"1", "true", "yes"}
    if not changed_files:
        if args.strict_no_empty or is_ci:
            print(
                "[ERROR] Changed files are empty. In CI/strict mode you must provide "
                "--base-ref/--head-ref or --changed-files-file."
            )
            return 1
        print("[OK] No changed files detected; required-update check skipped.")
        return 0

    errors: List[str] = []
    for rule in RULES:
        if not any_match(changed_files, rule.trigger_globs):
            continue
        missing = find_missing_required_files(changed_files, rule.required_files)
        if missing:
            errors.append(
                f"Rule '{rule.name}' triggered by {', '.join(rule.trigger_globs)}; "
                f"missing required updates: {', '.join(missing)}"
            )

    if errors:
        print("[ERROR] Required-update check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[OK] Required-update check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
