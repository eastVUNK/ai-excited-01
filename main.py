#!/usr/bin/env python3
"""Phoenix Moonburst entry: copy the validated image to /output/entry.png.

Reads phoenix.png from the repository, validates it (PNG signature, IHDR
1024x1024, size at most 1 MiB, IEND trailer), then writes the exact bytes
to the output directory. Deterministic: same input bytes, same output
bytes. Standard library only. No network, no clock, no randomness.
"""
import os
import struct
import sys

MAX_BYTES = 1048576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def read_entry_image():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "phoenix.png")
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail("cannot read phoenix.png: " + str(exc))
    if len(data) > MAX_BYTES:
        fail("phoenix.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != PNG_SIGNATURE:
        fail("phoenix.png is not a PNG file")
    if len(data) < 8 + 25 + 12:
        fail("phoenix.png is too short to hold an IHDR and IEND chunk")
    chunk_length, chunk_type = struct.unpack(">I4s", data[8:16])
    if chunk_type != b"IHDR" or chunk_length != 13:
        fail("first chunk is not a 13-byte IHDR")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        fail("phoenix.png is %dx%d, expected 1024x1024" % (width, height))
    if data[-12:-4] != struct.pack(">I4s", 0, b"IEND"):
        fail("phoenix.png has no IEND trailer")
    return data


def main():
    data = read_entry_image()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    tmp = target + ".tmp"
    with open(tmp, "wb") as handle:
        handle.write(data)
    os.replace(tmp, target)
    print("wrote %s (%d bytes)" % (target, len(data)))


if __name__ == "__main__":
    main()
