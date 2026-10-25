# Research index

The research lives in [phonedmrapp](https://github.com/IIMacGyverII/phonedmrapp); this is the map to it, with the
findings that decide what firmware can and cannot do. Dates are when the finding was measured.

## The module and its firmware

| Document (phonedmrapp) | What it settles |
|---|---|
| `docs/grok-deep-dive/11-firmware-fw0-results.md` | First analysis of the stock image: C-SKY V2 core, memory map, the UART dispatcher, the AT1846S driver, the channel handlers (2026-10) |
| `docs/deep-dive/19-firmware-modification-plan.md` | The plan for modifying the firmware, every step's status, and the running log of each image loaded (FW14 onward) |
| `radio_firmware/results.md` | Every bench measurement, image by image, with timestamps, hashes and end states |
| `radio_firmware/reviews.md` | The review of every step: what passed, what was wrong, what the next step is |
| `radio_firmware/symbols.csv` | Named addresses in the stock image |
| `tools/fw-patch/` | The patch table, stubs and build scripts that produce every modified image |
| `tools/fw-port/find_symbols.py` | Finds an image's anchors (version string, dispatch entries, time-out timer, free stub space) for a port to another phone |
| `radio_firmware/plan-port-automation.md` | How the next phone is ported with as little manual work as possible |
| `radio_firmware/plan-loader-safety.md` | The loader contract SignalDeck's firmware page is built against |
| `radio_firmware/plan-independent-m17-check.md` | Independent decoding of what we transmit: the MMDVM hotspot plan |

## Findings that shaped the images

- **The transmit audio path cannot carry digital modes** (cut below ~250 Hz is phone-side, ES8311), so digital
  transmit goes through the module's DMR modulator from TX RAM, fed by a symbol engine on command `0x40` (R3–R4t,
  2026-10-23/24; M17 1125 of 1125 frames).
- **Receive is flat with one register write held** (AT1846S `0x58` = `0xBCFD`) plus a fixed per-phone equaliser;
  M17 decodes at 98–100 % payload-exact to the squelch threshold (R-C to R-H, 2026-10-24).
- **The 30 s transmit limit was never in the firmware.** The stock app sends a time-out byte of 0, which turns the
  module's timer off; the module's own default is 120 s (FW19, 2026-10-24). 120 s at high power heats the Armor's AP
  zone by about 11 °C (2026-10-25).
- **Ending a transmission from firmware must run the stock unkey while the module still believes it is
  transmitting**, or the receiver stays off until a channel write (FW20, 2026-10-25).
- **Generic engines:** any rational symbol rate with a hold or polyphase pulse, and a phase-continuous tone queue,
  give POCSAG, Morse, RTTY and FT8 from the same command (FW21/FW22, 2026-10-25).
- **Update mode is a GPIO power-cycle with PTT held, then one byte, then plain YModem-1K with no checks**; the
  bootloader survives an interrupted transfer; the stock image cannot be read back (Phase E, 2026-10-25).

## Phones other than the Armor 26 Ultra

`docs/multi-device-xplore1-findings.md`, `docs/multi-device-atomxl-findings.md`, `docs/multi-device-armor3wt-findings.md`,
and the device pages under `../devices/`.

## Other modes on this hardware (for context)

`docs/m17-deep-dive-2026-10-22.md` and `docs/pocsag-deep-dive-2026-10-22.md` (what the audio path can and cannot do
before any firmware change), `docs/deep-dive/00-README.md` (the stock app and the LSPosed module, 14 chapters).
