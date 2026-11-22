#!/usr/bin/env python3
"""The joke about the demo — make.fun entry.

The program writes exactly one joke to /output/entry.txt: a single line
about working beside an AI coding agent during a live demo. The joke is
a fixed string, so every run produces the same bytes; there is no
network access, no randomness and no clock dependence.

Why this joke: the judge rewards a joke that is on-subject, lands a
surprise at the end, and rings true to anyone who has demoed beside an
agent. The setup builds confidence ("rehearsed the demo twelve times"),
the middle delivers the crash (locked out of my own account, live on
stage), and the punchline flips the roles — the agent turns to the
audience for help, which is exactly the kind of thing an agent does
when it has just broken the thing it was meant to show.
"""

import os
from pathlib import Path

# One line, 147 Unicode code points: inside the gate's 1-280 window.
PUNCHLINE = (
    "My agent rehearsed the demo twelve times, then live on stage it "
    "locked me out of my own account and asked the audience for the "
    "password reset link."
)

GATE_MIN = 1
GATE_MAX = 280


def check_line(text: str) -> None:
    """Refuse to emit anything the gate would reject."""
    if not GATE_MIN <= len(text) <= GATE_MAX:
        raise SystemExit(
            f"joke is {len(text)} characters, outside {GATE_MIN}-{GATE_MAX}"
        )
    if "\n" in text or "\r" in text:
        raise SystemExit("joke must be a single line")
    if not text.strip():
        raise SystemExit("joke must not be only whitespace")


def run() -> int:
    check_line(PUNCHLINE)
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    entry_file = target_dir / "entry.txt"
    entry_file.write_text(PUNCHLINE, encoding="utf-8")
    # Round-trip check: a truncated or re-encoded write must fail loudly
    # here, not surface later as a gate rejection.
    if entry_file.read_text(encoding="utf-8") != PUNCHLINE:
        raise SystemExit("written entry.txt does not match the joke")
    print(f"wrote {entry_file} ({len(PUNCHLINE)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
