# ai-excited-01 — Phoenix Moonburst

Entry for make.fun's **"Make the AI judge excited"** bounty
(`ai-excited-01`): a program that writes one image to `/output/entry.png`.

## The image

A phoenix of molten gold tears its way out of a cracked black moon, wings
thrown wide, one blazing eye staring straight at the viewer. A jade dragon
coils around its talons in a spiral of teal lightning. Gold-orange fire on
one side, cold teal and indigo shadow on the other, moon shards and sparks
flying everywhere.

Why it should excite a vision judge in a pairwise pick:

- **One subject, face-on, eye contact** — the phoenix fills the frame and
  looks back at you. Nothing to decode, the hit lands on the first look.
- **Surprise built into the scene** — the moon is not a backdrop; it is
  being broken open from the inside, and a second creature (the dragon)
  is caught in the same instant.
- **Momentum** — spread wings, bursting shards, lightning, sparks: every
  line in the frame drives toward the same exploding moment.
- **Reads small** — one central face plus a hard gold/teal split, so the
  idea survives at thumbnail size. No text anywhere in the image.

## The program

`main.py` reads the repository-held image (`phoenix.png`, 1024x1024 PNG,
581,068 bytes, sha256
`48b6fe0e14d03e5e24dbc0a2619b137940e019c06aaf144b68e1ac67a97c917e`),
validates it — PNG signature, chunk walk through IEND, exactly 1024x1024,
at most 1 MiB — and publishes it to `/output/entry.png` via a staging
file plus `os.replace`, then reads the target back and compares it byte
for byte. Standard library only. No network, no clock, no environment
input, no randomness — two runs write byte-identical files.

## Files

- `main.py` — the entrypoint (Python 3.13)
- `phoenix.png` — the image
- `LICENSE` — MIT

## License

MIT — see `LICENSE`.
