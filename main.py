#!/usr/bin/env python3
"""One Star, Written in Sap — make.fun entry.

Writes a single one-line 1-star review, in the voice of a houseplant
reviewing its human owner, to /output/entry.txt.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to 279
characters, not only white space, on a single line.
"""

import argparse
import sys
from pathlib import Path

ENTRY = (
    "One star. He waters me like an apology, moves me every time I start "
    "to thrive, and tells guests I'm 'low maintenance' while I sit in a "
    "mug with no drainage."
)

MAX_CHARS = 279
OUTPUT_PATH = Path("/output/entry.txt")


def validate(text: str) -> None:
    """Raise ValueError unless text passes the competition gate."""
    if not text:
        raise ValueError("entry is empty")
    if not text.strip():
        raise ValueError("entry is only white space")
    if len(text) != len(text.strip()):
        raise ValueError("entry has leading or trailing white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )


def write_entry(path: Path = OUTPUT_PATH) -> str:
    """Validate the line, write it, and confirm the file is byte-identical."""
    validate(ENTRY)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = ENTRY.encode("utf-8")
    path.write_bytes(data)
    back = path.read_bytes()
    if back != data:
        raise ValueError("written file differs from the entry line")
    # Runtime re-validation: decode what is actually on disk and run the
    # full gate over it, so a bad write can never pass silently.
    reread = back.decode("utf-8")
    validate(reread)
    if reread != ENTRY:
        raise ValueError("re-read entry differs from the entry line")
    return ENTRY


def self_test() -> bool:
    """Exercise the gate on the real line and on known-bad inputs."""
    validate(ENTRY)
    assert 1 <= len(ENTRY) <= MAX_CHARS
    assert ENTRY == ENTRY.strip() and "\n" not in ENTRY
    for bad in ("", "   ", "a" * 280, "two\nlines", " padded "):
        try:
            validate(bad)
        except ValueError:
            continue
        raise AssertionError(f"validate() accepted bad input: {bad!r}")
    return True


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Write the one-star houseplant review to /output/entry.txt."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run internal validation checks (no file written)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the existing /output/entry.txt without rewriting it",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        print(f"self-test OK: {len(ENTRY)} chars, single line, within gate")
        return 0

    if args.check:
        text = OUTPUT_PATH.read_text(encoding="utf-8")
        validate(text)
        if text != ENTRY:
            raise ValueError("existing entry.txt does not match the entry line")
        print(f"check OK: {len(text)} chars, single line, within gate")
        return 0

    line = write_entry()
    print(f"wrote {OUTPUT_PATH} ({len(line)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
