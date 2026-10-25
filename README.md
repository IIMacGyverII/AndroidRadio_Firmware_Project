# AndroidRadio Firmware Project

Stock and modified firmware for the radio modules inside Android walkie-talkie phones (Ulefone Armor 26 Ultra and
its relatives), with the device and module facts behind them, the catalogue that **SignalDeck** reads to offer and
verify images, and an index of the research that produced all of it.

This repository is the firmware home. The research and the bench live in
[phonedmrapp](https://github.com/IIMacGyverII/phonedmrapp); the app lives in
[SignalDeck](https://github.com/IIMacGyverII/SignalDeck).

## What is here

| Folder | Holds |
|---|---|
| `firmware/<device>/<tag>/` | One folder per image: the `.bin`, a `manifest.json` (hashes, base image, what it changes, where it was built), and a `README.md` for people |
| `catalog/` | `firmware.json` + `.sig`, the signed list SignalDeck fetches; how it is built, signed and published |
| `devices/<device>/` | One folder per phone: `README.md` (what is known, from which source, how far it is verified) and `device.json` (the same, machine-readable) |
| `modules/<module>/` | The radio module itself (HR-C7000 + AT1846S today): memory map, protocol, update mode, what the firmware does and does not do |
| `research/` | Index of the research behind every image, pointing into the phonedmrapp repository, with the findings that matter summarised |
| `scripts/` | Build, sign and verify the catalogue; verify a local image against it |
| `SAFETY.md` | What a user needs to know before loading anything, and what the loader checks for them |

## Status

| Device | Module | Stock image here | Modified images | Loader |
|---|---|---|---|---|
| Ulefone Armor 26 Ultra | HR-C7000 (`DMR003.UV4T.V022`) | yes | none released yet | SignalDeck, own YModem sender, proven 2026-10-25 |
| Ulefone Armor 20WT | HR-C7000 family (same stock app) | no | none | expected same as the 26 Ultra, unverified |
| Ulefone Armor 3WT | HR-C7000 family, Agold MCU over USB | no | none | not captured |
| Unihertz Atom XL | HR-C7000 (`DMR006.U4A.V082`), Agold MCU over USB | no | none | not captured |
| Blackview Xplore 1 | HR-C7000 family (same protocol) | no | none | expected similar, unverified |
| DOOGEE S80 | sibling protocol (RumiTX) | no | none | unknown |

**Only stock images and released images live here** (owner's rule). Bench and beta images stay in the phonedmrapp
repository until they are released. Nothing here changes band limits or output power, and nothing here is offered
to a phone whose module and stock app do not match the image's row exactly.

## How SignalDeck uses this repository

1. Reads `catalog/firmware.json` and checks its signature against the public key built into the app (the same key
   and format as its profile list).
2. Identifies the phone three ways (module version string, the stock app's own firmware asset, the phone model and
   stock package) and offers only rows whose base matches.
3. Saves the user's own vendor copy as the backup before anything else, downloads an image only from a catalogue
   row, checks the hash before and the version tag after, and restores the factory image on any mismatch.

The full contract is `SAFETY.md` here and `radio_firmware/plan-loader-safety.md` in phonedmrapp.

## Contributing an image or a device

- A device starts as `devices/<vendor>-<model>/README.md` written from a SignalDeck device report; say what was
  measured and what was only read.
- An image is added only when it is stock or released: with its manifest, its provenance (which repository, commit
  and build script produced it, byte for byte) and the results that measured it. Stock images carry the hash of the
  stock app asset they came from. Bench and beta images are not committed here.
- Never commit anything that identifies a person: callsigns, DMR IDs, locations, phone serials.
- Edit `CLAUDE.md` or `GROK.md`, then copy one over the other in the same commit (mirror rule).

## Licence

Our own files are GPL-3.0-or-later, like SignalDeck and phonedmrapp. Vendor firmware images are the property of
their makers and are redistributed unchanged for device owners' recovery and research; see `NOTICE.md`.
