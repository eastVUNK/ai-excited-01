#!/usr/bin/env python3
"""ai-excited-01 — hand the judge one image: "Phoenix Moonburst".

A phoenix of molten gold bursts out of a cracked black moon, one blazing
eye fixed on the viewer, while a jade dragon coils through teal lightning
at its talons. Gold fire against indigo shadow, a single central face, and
a moon broken open from the inside — built to hit on the first look, to
surprise, and to still read at 300 pixels wide.

The program itself does nothing clever on purpose. It takes the PNG that
ships in this repository, checks it against the bounty's limits, and
places a byte-for-byte copy at /output/entry.png. Standard library only;
no network, no clock, no environment input, no randomness, so every run
writes the exact same bytes.
"""

import os
import struct
import sys

# Image bundled with this repository, sitting beside this file.
IMAGE_NAME = "phoenix.png"

# The grader's output location.
OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.png"

# The bounty's limits for the image.
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_IMAGE_BYTES = 1024 * 1024

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
IHDR = b"IHDR"
IEND = b"IEND"


def _repo_path(name):
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, name)


def _load_image():
    """Read the bundled image off disk, failing loudly if it is absent."""
    path = _repo_path(IMAGE_NAME)
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError as exc:
        raise SystemExit("cannot read %s: %s" % (IMAGE_NAME, exc))


def _check_png(data):
    """Confirm the bytes are a complete 1024x1024 PNG under 1 MiB.

    Walks the chunk table from the signature through IEND, so a
    truncated or half-written file is caught instead of handed on.
    """
    if len(data) > MAX_IMAGE_BYTES:
        raise SystemExit(
            "image is %d bytes, over the 1 MiB limit" % len(data))
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("image does not start with the PNG signature")

    offset = len(PNG_MAGIC)
    width = height = None
    saw_iend = False
    while offset + 8 <= len(data):
        chunk_len = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        body_start = offset + 8
        body_end = body_start + chunk_len
        if body_end + 4 > len(data):
            raise SystemExit("PNG chunk %r runs past end of file" % chunk_type)
        if chunk_type == IHDR:
            if chunk_len != 13:
                raise SystemExit("PNG IHDR has unexpected length %d" % chunk_len)
            width, height = struct.unpack(">II", data[body_start:body_start + 8])
        if chunk_type == IEND:
            saw_iend = True
            break
        offset = body_end + 4  # skip the chunk's CRC

    if width is None:
        raise SystemExit("PNG has no IHDR chunk")
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            "image is %dx%d, expected %dx%d"
            % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT))
    if not saw_iend:
        raise SystemExit("PNG is missing its IEND chunk")


def _publish(data):
    """Write the image atomically to the grader's output path.

    After the rename, the target is read back and compared byte for
    byte, so a short write or a bad disk is caught here instead of
    silently handing the judge a broken file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    target = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
    staging = target + ".staging"
    with open(staging, "wb") as handle:
        handle.write(data)
    os.replace(staging, target)
    with open(target, "rb") as handle:
        written = handle.read()
    if written != data:
        raise SystemExit("published image differs from the source bytes")
    return target


def main(argv=None):
    del argv  # the entry takes no arguments; the image is fixed.
    data = _load_image()
    _check_png(data)
    _publish(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
