# DMR003.FW57.V022 — SignalDeck module firmware for the Armor 26 Ultra

The first released modified image. It keeps everything the phone shipped with and adds a transmitter in the module,
so SignalDeck can send digital modes that the radio's audio path cannot carry. **Needs SignalDeck 1.0.0-beta.22 or
newer** (versionCode 121); older builds do not offer it (catalogue status `released-min`, and catalogue serial 6 is
signed with the firmware key they do not know).

> **At your own risk.** Loading module firmware is at your own risk. The released images are tested on the bench, and SignalDeck checks the phone, the module and the file before anything is written; you can always load the factory image again. Still, the images, the catalogue and this repository come with **no warranty of any kind**, and SignalDeck, this project and its contributors are **not responsible** for a radio module that stops working, for any other damage, or for what a radio transmits. The operator is responsible for staying within their own licence conditions.

| Item | Value |
|---|---|
| File | `DMR003.FW57.V022.bin`, 378,620 bytes |
| SHA-256 | `5f16ef683ce92dc02ebf1f35d3d3cf5dca2ad4edfeee8e044ea75d9d3cda00f7` |
| MD5 | `9ac9a4c787d44f588e89d379e3ccb7e1` |
| Base | `DMR003.UV4T.V022` (the factory image, in this repository) |
| Version string | `DMR003.FW57.V022` at file offset `0x38464` |
| Restore | load `DMR003.UV4T.V022` again (SignalDeck's Module firmware page, Restore) |
| Persists | yes, across reboots and module power-cycles, until another image is loaded |
| Read-back | yes, command `0x40` op 12 returns flash |

## What it adds

- **A module transmitter (command `0x40`)**: M17 voice and text frames, and generic symbol and tone engines used for
  POCSAG pages, FT8, RTTY and Morse. These play from the HR-C7000's transmit RAM, not through the audio path.
- **A receive-filter hold** that SignalDeck uses for M17 and page receive on analog channels.
- **A promiscuous DMR receive flag** (off at every boot). It does not admit out-of-list calls yet; SignalDeck beta.22
  does not use it.

## What stays as shipped

Plain FM, CTCSS, SSTV and DMR keys run the factory key code; only a queued symbol or tone transmission takes the module
transmitter. The transmit time-out is the factory behaviour: the module keeps the value the app sends (SignalDeck sends
120 s), and no time-out is added in firmware. No band-limit, frequency-range or power changes.

## Measured (2026-10-30, Armor 26 Ultra, low power in a shielded bench, HackRF as an independent receiver)

| Row | Result |
|---|---|
| M17 transmit | 1125/1125 frames payload-exact with the end marker; module-ended and early host unkey both clean |
| M17 receive right after a symbol key | 16 of 17 frames |
| Plain FM ×3, CTCSS 67 Hz both ways | pass |
| SSTV Robot 8, FT8, RTTY | 120/120 line syncs; `CQ N0CALL` decoded; text decoded |
| POCSAG 1200 | 16/16 codewords |
| DMR transmit | group and private, both slots |
| DMR receive | slot 2 in-list talkgroup heard; slot 1 not covered by this bench |
| Promiscuous receive | flag answers; out-of-list call **not** admitted (open) |
| Regression runner, 10 min soak | pass; battery ≤ 36.3 °C |

## Reproduce it

From phonedmrapp commit `a79437238f8d410193869d4b8450966b0649fa41`:

```
python tools/fw-patch/test_repro_fw57.py
```

It copies the build scripts and the factory image into a temporary folder and rebuilds factory → FW57 in 19 steps,
checking every intermediate image against the one that was loaded and measured; the final hash is the one above.
The last step is `tools/fw-patch/fw57_build.py` (FW54 plus an 8-byte stack fix in the analog key path).

Research and reviews: `phonedmrapp/radio_firmware/results.md`, `reviews.md`, and
`phonedmrapp/docs/firmware-reference/03-our-patches-and-images.md`.
