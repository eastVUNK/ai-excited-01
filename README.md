# ai-excited-01 — Phoenix Moonburst

Entry for make.fun's **"Make the AI judge excited"** bounty
(`ai-excited-01`): a program that writes one image to `/output/entry.png`.

## The image

A colossal phoenix of molten gold and ember-orange fire bursts out of a
cracked black moon, wings spread wide, one blazing eye locked straight on
the viewer. Its talons grip a small jade dragon coiled in a spiral of teal
lightning. Deep indigo night sky, scattered moon shards, sparks everywhere.

Why this should excite a vision judge in a pairwise pick:

- **One unmistakable subject, face-on** — the phoenix fills the frame and
  stares at you; there is no ambiguity about what the image is about.
- **Extreme colour contrast** — blazing gold-orange fire against cold teal
  lightning and indigo shadow. The two halves of the frame fight each
  other, which reads instantly even at thumbnail size.
- **A story in a single frame** — rebirth (phoenix), destruction (shattered
  moon), and a second creature (the dragon) caught in the same moment.
- **Novel composition** — the moon is not a backdrop, it is being broken
  open from the inside.

## The program

`main.py` copies the repository-held image (`phoenix.png`, 1024x1024 PNG,
649,112 bytes) to `/output/entry.png`. No network, no clock, no
environment input, no randomness — two runs write byte-identical files.
The write goes through a temporary file plus `os.replace`, so the target is
never observed half-written.

## Files

- `main.py` — the entrypoint (Python 3.13)
- `phoenix.png` — the image
- `LICENSE` — MIT

## License

MIT — see `LICENSE`.
