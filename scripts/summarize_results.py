"""Compatibility entrypoint for experiment result summarization."""

from __future__ import annotations

from pathlib import Path
import sys


def _resolve_main():
    """Resolve main entrypoint for both module and script invocation."""
    if __package__:
        from .experiment.reporting.summarizer import main as resolved_main

        return resolved_main

    repo_root = Path(__file__).resolve().parents[1]
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)
    from scripts.experiment.reporting.summarizer import main as resolved_main

    return resolved_main


main = _resolve_main()


if __name__ == "__main__":
    main()
