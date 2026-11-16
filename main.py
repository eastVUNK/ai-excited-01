#!/usr/bin/env python3
"""ai-excited-01 entry: publish the repo-held Phoenix Moonburst PNG.

Reads phoenix.png from this repository, validates its PNG header
(1024x1024, at most 1 MiB, proper IEND trailer), then writes it to
/output/entry.png with a plain open + os.replace.

Standard library only. No network, clock, environment or randomness:
every run writes the same bytes.
"""
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "phoenix.png")
DST = "/output/entry.png"
MAX_BYTES = 1_048_576
IEND_TAIL = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        raise SystemExit("phoenix.png exceeds 1 MiB")
    if len(data) < 33:
        raise SystemExit("phoenix.png is truncated")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("phoenix.png is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit("unexpected image size %dx%d" % (width, height))
    if data[-12:] != IEND_TAIL:
        raise SystemExit("phoenix.png lacks a proper IEND trailer")
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    tmp = DST + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, DST)


if __name__ == "__main__":
    main()
