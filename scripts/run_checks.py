"""Run all repository checks with one command.

Default checks:
1) Language policy check
2) Output schema check
3) Documentation sync check
4) Pipeline freshness check
5) Plan coverage check
6) Result traceability check
7) Required updates check
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Run all repository checks.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("output"),
        help="Output root used by output schema checker.",
    )
    parser.add_argument(
        "--allow-placeholder",
        action="store_true",
        help="Allow simulated placeholder outputs in schema checks.",
    )
    return parser.parse_args()


def run_check(command: List[str]) -> Tuple[int, str]:
    """Run one check command and return (exit_code, printable command)."""
    printable = " ".join(command)
    result = subprocess.run(command, check=False)
    return result.returncode, printable


def main() -> int:
    """Run all checks in order and return non-zero on any failure."""
    args = parse_args()

    checks = [
        [
            sys.executable,
            "scripts/checks/check_language_policy.py",
        ],
        [
            sys.executable,
            "scripts/checks/check_output_schema.py",
            "--output-root",
            str(args.output_root),
        ]
        + (["--allow-placeholder"] if args.allow_placeholder else []),
        [
            sys.executable,
            "scripts/checks/check_doc_sync.py",
        ],
        [
            sys.executable,
            "scripts/checks/check_pipeline_freshness.py",
            "--output-root",
            str(args.output_root),
        ],
        [
            sys.executable,
            "scripts/checks/check_plan_coverage.py",
            "--output-root",
            str(args.output_root),
        ],
        [
            sys.executable,
            "scripts/checks/check_result_traceability.py",
        ],
        [
            sys.executable,
            "scripts/checks/check_required_updates.py",
        ],
    ]

    has_failure = False
    for command in checks:
        print(f"[RUN] {' '.join(command)}")
        code, printable = run_check(command)
        if code != 0:
            has_failure = True
            print(f"[FAIL] {printable}")
        else:
            print(f"[OK] {printable}")

    if has_failure:
        print("[ERROR] One or more checks failed.")
        return 1

    print("[OK] All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
