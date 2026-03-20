"""Validate repository language policy for code, notebooks, and docs.

Policy summary:
- Python comments, docstrings, and print/log messages must be English (no CJK chars).
- Notebook markdown cells must be Chinese (must contain at least one CJK char).
- Notebook code comments and print/log strings should be English (no CJK chars).
- `spec/` markdown must be English-only (no CJK chars).
- `docs/` markdown should be Chinese-primary (contains at least one CJK char).
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import tokenize
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


HAN_RE = re.compile(r"[\u4e00-\u9fff]")
LOG_METHODS = {"debug", "info", "warning", "error", "exception", "critical"}


def has_han(text: str) -> bool:
    """Return True when text contains Han characters."""
    return bool(HAN_RE.search(text))


def iter_python_files(paths: Sequence[Path]) -> Iterable[Path]:
    """Yield python files from provided paths."""
    for path in paths:
        if path.is_file() and path.suffix == ".py":
            yield path
            continue
        if path.is_dir():
            for file_path in path.rglob("*.py"):
                if any(part in {".git", ".venv", "__pycache__", "model"} for part in file_path.parts):
                    continue
                yield file_path


def iter_notebooks(paths: Sequence[Path]) -> Iterable[Path]:
    """Yield notebook files from provided paths."""
    for path in paths:
        if path.is_file() and path.suffix == ".ipynb":
            yield path
            continue
        if path.is_dir():
            for file_path in path.rglob("*.ipynb"):
                if ".ipynb_checkpoints" in file_path.parts:
                    continue
                yield file_path


def iter_markdown_files(path: Path) -> Iterable[Path]:
    """Yield markdown files recursively from a directory."""
    if not path.exists() or not path.is_dir():
        return []
    return path.rglob("*.md")


def check_python_comments(path: Path) -> List[str]:
    """Check comments for Han characters."""
    issues: List[str] = []
    with path.open("rb") as f:
        for token in tokenize.tokenize(f.readline):
            if token.type == tokenize.COMMENT and has_han(token.string):
                issues.append(f"{path}:{token.start[0]} comment contains non-English text")
    return issues


def extract_call_string(node: ast.AST) -> str:
    """Extract string content from AST string-like expressions."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts: List[str] = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
        return "".join(parts)
    return ""


def iter_docstrings(tree: ast.AST) -> Iterable[Tuple[str, int, str]]:
    """Yield (kind, line, docstring) tuples for module/class/function docstrings."""
    module_doc = ast.get_docstring(tree)
    if module_doc:
        yield ("module", 1, module_doc)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node)
            if doc:
                yield (type(node).__name__, node.lineno, doc)


def check_python_docstrings_and_outputs(path: Path) -> List[str]:
    """Check docstrings and print/log strings for Han characters."""
    issues: List[str] = []
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    for kind, line, doc in iter_docstrings(tree):
        if has_han(doc):
            issues.append(f"{path}:{line} {kind} docstring contains non-English text")

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        is_print = isinstance(node.func, ast.Name) and node.func.id == "print"
        is_log = (
            isinstance(node.func, ast.Attribute)
            and node.func.attr in LOG_METHODS
        )
        if not (is_print or is_log):
            continue

        if not node.args:
            continue

        first_arg = extract_call_string(node.args[0])
        if first_arg and has_han(first_arg):
            call_type = "print" if is_print else "log"
            issues.append(f"{path}:{node.lineno} {call_type} message contains non-English text")

    return issues


def check_notebook(path: Path) -> List[str]:
    """Check notebook markdown and code cell language policy."""
    issues: List[str] = []
    nb = json.loads(path.read_text(encoding="utf-8"))
    for idx, cell in enumerate(nb.get("cells", []), start=1):
        source = "".join(cell.get("source", []))
        if not source.strip():
            continue

        if cell.get("cell_type") == "markdown":
            if not has_han(source):
                issues.append(f"{path}:cell{idx} markdown cell lacks Chinese text")
            continue

        if cell.get("cell_type") != "code":
            continue

        for line_no, line in enumerate(source.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#") and has_han(stripped):
                issues.append(f"{path}:cell{idx}:{line_no} code comment contains non-English text")

        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not node.args:
                continue
            is_print = isinstance(node.func, ast.Name) and node.func.id == "print"
            is_log = isinstance(node.func, ast.Attribute) and node.func.attr in LOG_METHODS
            if not (is_print or is_log):
                continue
            text = extract_call_string(node.args[0])
            if text and has_han(text):
                issues.append(f"{path}:cell{idx}:{node.lineno} code output text contains non-English text")

    return issues


def check_spec_docs_english(path: Path) -> List[str]:
    """Ensure spec markdown is English-only (no Han chars)."""
    issues: List[str] = []
    for md_file in iter_markdown_files(path):
        text = md_file.read_text(encoding="utf-8")
        if has_han(text):
            issues.append(f"{md_file} contains non-English text in spec/")
    return issues


def check_docs_primary_chinese(path: Path) -> List[str]:
    """Ensure docs markdown is Chinese-primary (contains Han chars)."""
    issues: List[str] = []
    for md_file in iter_markdown_files(path):
        text = md_file.read_text(encoding="utf-8")
        if text.strip() and not has_han(text):
            issues.append(f"{md_file} lacks Chinese text in docs/")
    return issues


def main() -> int:
    """Run checks and return process exit code."""
    parser = argparse.ArgumentParser(description="Check language policy for code and notebooks.")
    parser.add_argument(
        "--paths",
        nargs="+",
        default=["scripts", "efficient_kan", "verify_install.py", "notebooks"],
        help="Paths to check.",
    )
    args = parser.parse_args()

    check_paths = [Path(p) for p in args.paths]
    issues: List[str] = []

    for py_file in iter_python_files(check_paths):
        issues.extend(check_python_comments(py_file))
        issues.extend(check_python_docstrings_and_outputs(py_file))

    for nb_file in iter_notebooks(check_paths):
        issues.extend(check_notebook(nb_file))

    issues.extend(check_spec_docs_english(Path("spec")))
    issues.extend(check_docs_primary_chinese(Path("docs")))

    if issues:
        print("[FAIL] Language policy violations detected:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("[OK] Language policy checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
