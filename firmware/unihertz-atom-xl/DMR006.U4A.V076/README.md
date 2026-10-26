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
`0x0301A000`. It has a 6 KiB zero run at `+0x55ED2`. How the stock app's `updateDmr` reaches the module through
the phone's USB bridge MCU is not captured yet.

**Command dispatch (read 2026-10-26, C-SKY objdump; `phonedmrapp/tools/fw-port/find_symbols.py --switch`):** the
same idiom as the Armor's. The command byte goes through `subi r3, 34; cmphsi r3, 103; lrw r2, table;
ldr.w r3, (r2, r3 << 2); jmp r3` (jump at `+0xA038`) into a jump table at file `+0x33274`: 103 cases for commands
0x22–0x88, with the unknown-command case at `+0x9FE0`. Each case is an 8-byte thunk `mov r0, r4; bsr handler;
pop r4-r5, r15`. The Armor's thunks end `pop r4-r8, r15`.

| Command | Case | Handler | Named by |
|---|---|---|---|
| `0x3B` set time-out | `+0xA058` | `+0x9A5C` | loads the time-out struct `0x38AF8` (the Armor's handler is `+0xA308`, struct `0x38C64`) |
| `0x34` version | `+0xA09C` | `+0x9F18` | loads the version string address `0x0304D410` = file `+0x33410` (the Armor's is `+0xA7E8`) |

The Armor's `0x3D`–`0x3F` and `0x46` have no case of their own on V076, and its table ends at `0x88`.

**Not for loading or patching.** V076 is the vendor partition's updater copy; the phone's module runs
`DMR006.U4A.V082`. Nothing from this reading may be built for or loaded on an Atom XL until V082 is obtained and
diffed. The offsets above are V076's only.

The phone's five bridge MCU images (Cortex-M, `/vendor/data/mcu/`) are not module images and are not kept here.
Findings: `phonedmrapp/docs/multi-device-atomxl-findings.md`.
