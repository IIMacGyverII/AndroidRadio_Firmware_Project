# Changelog

Newest first. One entry per change that a user of SignalDeck or a reader of the repository would notice.

## 2026-10-28 — Atom XL: module versions vary per unit; the running image is not on the phone

- `devices/unihertz-atom-xl/variants.json`: variant `DMR006.U4A.V067`, measured on a bench Atom XL (not supported, no
  image). V076's note now says the module runs V082 on one phone and V067 on another.
- `devices/unihertz-atom-xl/README.md`: per-unit module version, bridge MCU (USB `0483:5730`), 32 kHz USB audio, the
  USB host-mode switch while the radio is on, the PTT key, and where the running image was looked for and not found.
- Catalogue serial 6.

## 2026-10-26 — Atom XL module image (research copy)

- `firmware/unihertz-atom-xl/DMR006.U4A.V076/`: the module image an Atom XL keeps on its vendor partition, byte for
  byte, with manifest and README. It is older than the V082 the phone's module runs, so it is `factory: false` and
  SignalDeck does not offer it for loading.
- `devices/unihertz-atom-xl/`: the V076 variant and where it came from.
- `scripts/build_catalog.py`: a manifest may name its own `tagOffset` (this image's version string is at `0x33410`).
- Catalogue serial 5.

## 2026-10-25 — Registry, keys, recovery, templates, CI

- Variant registry: `devices/<device>/variants.json` for every module version and stock asset seen on a model,
  folded into the signed catalogue (`variants`), with `devices/VARIANTS.md`.
- Public signing key published (`catalog/public_key.pem`, fingerprint in `catalog/VERIFY.md`) with verification
  instructions; `catalog/KEYS.md` records custody, the planned separate firmware key, and rotation.
- `RECOVERY.md` for a module that no longer answers.
- `devices/TEMPLATE.md` and `devices/device.schema.json`; GitHub issue forms and a pull-request checklist.
- CI (`.github/workflows/check.yml`): manifests match their files, the committed catalogue matches the manifests,
  the signature verifies, the agent files are mirrored, no bench or beta image is present.
- `SAFETY.md`: the owner's rule for loading your own image (Advanced switch, off by default, two confirmations,
  hash typed, all other checks kept).
- `research/METHODS.md`: the bench, the reading, the build, the test order, heat, the loader proofs, the process.
- Catalogue serial 3 (serial 2 was signed over CRLF bytes and never valid on a Linux checkout; the builder now writes LF and `.gitattributes` keeps the catalogue files byte-exact).

## 2026-10-25 — Repository created

- Layout: `firmware/`, `catalog/`, `devices/`, `modules/`, `research/`, `scripts/`, with `SAFETY.md` and `NOTICE.md`.
- Images: Ulefone Armor 26 Ultra stock `DMR003.UV4T.V022` with manifest and provenance. Bench and beta images are
  not committed here (owner's rule); released images will be.
- Catalogue `firmware.json` serial 1, signed with the SignalDeck profile-list key.
- Devices: Armor 26 Ultra (verified), Armor 20WT, Armor 3WT, Atom XL, Xplore 1, DOOGEE S80 (from reports and stock
  apps, unverified).
- Module: HR-C7000 + AT1846S facts, including update mode and the bootloader handshake.
