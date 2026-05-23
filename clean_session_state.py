#!/usr/bin/env python3
"""
clean_session_state.py — Strip ungraceful exit noise from SESSION_STATE.md

Usage:
    python3 clean_session_state.py [path/to/SESSION_STATE.md]

Default path: SESSION_STATE.md in the current directory.

What it removes:
    All "## ⚠️ Ungraceful exit" blocks (header + Branch + session-close lines)
    that are appended automatically when a Claude Code session exits without
    running /session-close.

What it keeps:
    All structured content: phase, tests, plans, invariants, decisions, bugs,
    and proper session entries (## Session NNN — ...).
"""

import re
import sys
from pathlib import Path


def clean(path: Path) -> None:
    text = path.read_text()
    lines = text.splitlines()

    keep = []
    skip = False

    for line in lines:
        if line.startswith("## ⚠️"):
            skip = True
            continue
        # Stop skipping when a real section header appears
        if skip and line.startswith("## ") and "⚠️" not in line:
            skip = False
        if skip:
            continue
        keep.append(line)

    result = "\n".join(keep)
    # Collapse runs of 3+ blank lines into 2
    result = re.sub(r"\n{3,}", "\n\n", result)

    path.write_text(result.rstrip() + "\n")
    print(f"Cleaned {path} — {len(lines)} → {len(result.splitlines())} lines")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("SESSION_STATE.md")
    if not target.exists():
        print(f"Error: {target} not found", file=sys.stderr)
        sys.exit(1)
    clean(target)
