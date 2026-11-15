#!/usr/bin/env python3
"""ai-excited-01: write one image that excites the AI judge.

The entry is a program that writes a single 1024x1024 PNG to
/output/entry.png. The image itself lives in this repository as
``phoenix.png``: a phoenix of molten gold bursting out of a cracked black
moon, one blazing eye locked on the viewer, a jade dragon coiled in teal
lightning around its talons. Fire against ice, gold against indigo — the
kind of single-frame drama that wins a pairwise pick.

The program is deliberately boring: it copies the repository-held bytes to
the output path with no network, no clock, no environment input and no
randomness, so two runs write byte-identical files.
"""

import os
import struct

# The image this entry hands to the judge, stored next to this file.
_SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phoenix.png")

# Where the grader expects the entry image.
_TARGET = "/output/entry.png"

# The contract the bounty sets for the image: exactly 1024x1024, PNG,
# at most 1 MiB. Checked from the PNG header with the standard library
# only, so the entry needs no third-party package at run time.
_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_MAX_BYTES = 1024 * 1024


def _check_png(data: bytes) -> None:
    """Fail fast if the repo-held image is not a 1024x1024 PNG."""
    if len(data) > _MAX_BYTES:
        raise ValueError("image exceeds 1 MiB: %d bytes" % len(data))
    if not data.startswith(_PNG_SIGNATURE):
        raise ValueError("image is not a PNG")
    # IHDR chunk: width and height are the first 8 bytes of its data.
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise ValueError("image is %dx%d, expected 1024x1024" % (width, height))


def main() -> None:
    with open(_SOURCE, "rb") as source:
        data = source.read()
    _check_png(data)

    os.makedirs(os.path.dirname(_TARGET), exist_ok=True)

    # Write to a temporary file in the same directory, then atomically
    # replace the target, so a reader never sees a half-written image.
    tmp = _TARGET + ".tmp"
    with open(tmp, "wb") as out:
        out.write(data)
    os.replace(tmp, _TARGET)


if __name__ == "__main__":
    main()
