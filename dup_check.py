#!/usr/bin/env python3
"""dup_check.py

A tiny utility that scans a text file for duplicate lines.

Features:
- Proactive error detection (missing file, permission errors, empty input).
- Clear naming conventions for readability.
- Idempotent output – running multiple times on the same file yields the same result.

Usage:
    python3 dup_check.py <path-to-file>
"""

import sys
import os
from collections import defaultdict
from typing import List, Dict

def _load_file_lines(path: str) -> List[str]:
    """Read *path* and return a list of its lines.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError:  If the file cannot be read.
        ValueError:        If the file is empty.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Cannot read file (permission denied): {path}")
    with open(path, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
    if not lines:
        raise ValueError(f"File is empty: {path}")
    # Strip trailing newlines but preserve original whitespace for exact matching
    return [line.rstrip('\n') for line in lines]

def _find_duplicates(lines: List[str]) -> Dict[str, List[int]]:
    """Return a mapping of line content -> list of 1‑based line numbers where it appears.

    Only entries with more than one occurrence are retained.
    """
    occurrence_map: Dict[str, List[int]] = defaultdict(list)
    for idx, line in enumerate(lines, start=1):
        occurrence_map[line].append(idx)
    # Filter out unique lines
    duplicates = {text: nums for text, nums in occurrence_map.items() if len(nums) > 1}
    return duplicates

def _print_report(duplicates: Dict[str, List[int]]) -> None:
    """Print duplicate information to stdout.

    If *duplicates* is empty, a clean‑file message is shown.
    """
    if not duplicates:
        print("No duplicate lines found. File is clean.")
        return
    for text, nums in sorted(duplicates.items()):
        line_list = ", ".join(map(str, nums))
        print(f'Duplicate line "{text}" found on lines: {line_list}')

def main(argv: List[str] | None = None) -> int:
    """Entry point for the script.

    Returns an exit code (0 = success, 1 = error).
    """
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python3 dup_check.py <path-to-file>")
        return 1
    file_path = argv[0]
    try:
        lines = _load_file_lines(file_path)
        duplicates = _find_duplicates(lines)
        _print_report(duplicates)
        return 0
    except (FileNotFoundError, PermissionError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1
    except Exception as exc:  # Catch‑all for unforeseen errors, but still report
        print(f"Unexpected error: {exc}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
