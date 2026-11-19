#!/usr/bin/env python3
"""Entry point for the news-image-20261119 bounty (Python 3.13, stdlib only).

The infographic itself is drawn by render.py and shipped in this repo as
entry.png. All this program does is place an exact copy of that image at
$MAKEFUN_OUTPUT_DIR/entry.png (falling back to /output when the variable
is unset), so repeated runs always produce identical bytes.
"""

from pathlib import Path

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
FALLBACK_DIR = Path("/output")


def resolve_destination() -> Path:
    """Work out where the copy has to land, creating the folder if needed."""
    import os

    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    base = Path(raw) if raw else FALLBACK_DIR
    base.mkdir(parents=True, exist_ok=True)
    return base / OUTPUT_NAME


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    payload = source.read_bytes()
    destination = resolve_destination()
    destination.write_bytes(payload)
    print(f"copied {source} -> {destination} ({len(payload)} bytes)")


if __name__ == "__main__":
    main()
