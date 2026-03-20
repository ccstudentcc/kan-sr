"""Check whether execution scripts are documented in core project docs.

This gate prevents code/doc drift by discovering pipeline scripts automatically
instead of relying on a fixed hard-coded script list.
"""

from __future__ import annotations

import argparse
import fnmatch
import sys
from pathlib import Path
from typing import List


DEFAULT_INCLUDE_GLOBS = [
    "run_*.py",
    "summarize_*.py",
    "check_*.py",
    "run_checks.py",
]

DEFAULT_EXCLUDE_SCRIPTS = [
    "check_doc_sync.py",
]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate documentation sync for core execution scripts."
    )
    parser.add_argument(
        "--protocol-doc",
        type=Path,
        default=Path("EXPERIMENT_PROTOCOL.md"),
        help="Path to protocol document.",
    )
    parser.add_argument(
        "--status-doc",
        type=Path,
        default=Path("CURRENT_WORK_REFERENCE.md"),
        help="Path to status/reference document.",
    )
    parser.add_argument(
        "--scripts-dir",
        type=Path,
        default=Path("scripts"),
        help="Directory where executable scripts are discovered.",
    )
    parser.add_argument(
        "--include-globs",
        nargs="+",
        default=DEFAULT_INCLUDE_GLOBS,
        help="Filename glob patterns for scripts that must be documented in both docs.",
    )
    parser.add_argument(
        "--exclude-scripts",
        nargs="+",
        default=DEFAULT_EXCLUDE_SCRIPTS,
        help="Script filenames to exclude from documentation sync checks.",
    )
    return parser.parse_args()


def load_text(path: Path) -> str:
    """Load text content from a markdown document."""
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")
    return path.read_text(encoding="utf-8")


def discover_required_scripts(
    scripts_dir: Path, include_globs: List[str], exclude_scripts: List[str]
) -> List[str]:
    """Discover required script filenames using include/exclude patterns."""
    if not scripts_dir.exists() or not scripts_dir.is_dir():
        raise FileNotFoundError(f"Scripts directory not found: {scripts_dir}")

    discovered: List[str] = []
    for file_path in sorted(scripts_dir.rglob("*.py")):
        name = file_path.name
        if name in exclude_scripts:
            continue
        if any(fnmatch.fnmatch(name, pattern) for pattern in include_globs):
            discovered.append(name)
    return discovered


def find_missing_references(doc_text: str, required_scripts: List[str]) -> List[str]:
    """Return required script names that are missing from a document."""
    return [name for name in required_scripts if name not in doc_text]


def main() -> int:
    """Run doc-sync checks and return process exit code."""
    args = parse_args()
    errors: List[str] = []

    try:
        protocol_text = load_text(args.protocol_doc)
        status_text = load_text(args.status_doc)
        required_scripts = discover_required_scripts(
            args.scripts_dir, args.include_globs, args.exclude_scripts
        )
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        return 1

    if not required_scripts:
        print("[ERROR] No required scripts discovered. Check include globs or scripts directory.")
        return 1

    missing_in_protocol = find_missing_references(protocol_text, required_scripts)
    missing_in_status = find_missing_references(status_text, required_scripts)

    if missing_in_protocol:
        errors.append(
            f"{args.protocol_doc} is missing script references: {', '.join(missing_in_protocol)}"
        )
    if missing_in_status:
        errors.append(
            f"{args.status_doc} is missing script references: {', '.join(missing_in_status)}"
        )

    if errors:
        print("[ERROR] Documentation sync check failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("[OK] Documentation sync check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
