# DMR006.U4A.V076 — an Atom XL module image from the vendor partition

A stock module image for the Unihertz Atom XL, kept for research. **It is not the phone's factory image and is not
offered for loading** (`factory: false`, and its base is not one SignalDeck lists): the module in the phone it came
from reports `DMR006.U4A.V082`, a newer build. This file is the copy the phone keeps on its vendor partition for the
stock app's updater.

| Item | Value |
|---|---|
| File | `DMR006.U4A.V076.bin`, 358,100 bytes |
| SHA-256 | `4f5f287bef875fad4a5c8ca9a94c9e841a21f5b507f2cc2a0645d5947e4d40fe` |
| MD5 | `61fd4306ca518f2ed4c30b583d810b58` |
| Taken from | an Atom XL's `/vendor/data/DMR/dmr/DMR006.U4A.V076.bin`, byte for byte (2026-10-26); not an asset of the stock app `com.agold.intercom` 2.0, whose APK carries no image |
| Version string | `DMR006.U4A.V076` at file offset `0x33410` (the Armor's image has its string at `0x38464`, so the manifest names its own `tagOffset`) |
| Transmit time-out | not measured |
| Read-back | no (stock firmware) |

**What is known (read offline, nothing run on an Atom XL):** the first 64 bytes are identical to the Armor 26
Ultra's `DMR003.UV4T.V022` (C-SKY V2 start-up code, the HR-C7000 family) and it runs from the same XIP base
`0x0301A000`. `phonedmrapp/tools/fw-port/find_symbols.py` finds the time-out timer (struct `0x38AF8`) and a 6 KiB
zero run at `+0x55ED2`, but not the command dispatch table, so the Armor's patches do not apply to it. How the stock
app's `updateDmr` reaches the module through the phone's USB bridge MCU is not captured yet.

The phone's five bridge MCU images (Cortex-M, `/vendor/data/mcu/`) are not module images and are not kept here.
Findings: `phonedmrapp/docs/multi-device-atomxl-findings.md`.
