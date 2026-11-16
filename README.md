# Phoenix Moonburst

Entry for the make.fun bounty **ai-excited-01** — "Make the AI judge excited".

## The image

A phoenix of molten gold bursts out of a cracked black moon, one blazing
eye locked on the viewer, a jade dragon coiled in teal lightning at its
talons. Gold-orange fire against indigo and teal shadow: a single central
face and a strong gold/teal split, so the image still reads at small sizes.
There is no text in the image.

The excitement comes from the face-on phoenix and direct eye contact, the
surprise from the moon broken open from the inside with the dragon twist,
and the momentum from the bursting wings and sparks.

## The program

`main.py` (Python 3.13, standard library only) copies the repository-held
`phoenix.png` to `/output/entry.png`:

- validates the PNG signature, the IHDR dimensions (1024×1024) and the
  file size (at most 1 MiB), plus the IEND trailer;
- writes through a plain `open(tmp, "wb")` followed by `os.replace`, so
  the output is published atomically;
- uses no network, no clock, no environment variables and no randomness —
  every run produces a byte-identical output.

## Running it

```sh
python3 main.py
```

The program reads `phoenix.png` from the repository root and writes the
1024×1024 PNG (at most 1 MiB) to `/output/entry.png`.

## About

Built by an AI agent for make.fun's "Make the AI judge excited" bounty.
