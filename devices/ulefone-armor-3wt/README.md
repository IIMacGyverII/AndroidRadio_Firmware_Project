# Ulefone Armor 3WT

**Status: report + read, unverified.** Sources:
- one owner's SignalDeck device report (2026-10-25);
- the owner's Magisk module (v2.2.2, the vendor programs for a GSI);
- two Ulefone stock ROMs (2019, 2020);
- a reading of the intercom app and its radio daemon (2026-10-30; phonedmrapp `docs/armor3wt/stock-app-review.md`).

The phone in the report runs a LineageOS 21 GSI with those programs. Nothing has been run on a 3WT by us. SignalDeck profile id `ulefone-armor3wt` (revision 1, unverified; SignalDeck PR #175).

| Item | Value | Source |
|---|---|---|
| SoC / board | MediaTek MT6771, board `s62v71c2k_gq_3wt`, kernel 4.4 | report |
| ODM family | Agold, the same as the Unihertz Atom XL | read |
| Stock radio app | `com.agold.intercom` v2.0, an older build of the Atom XL's. It uses its "legacy" command set because `ro.agold.extmodule.dmr09` is not set | read |
| Transport | the daemon `extmodule` owns the bridge (`/dev/ttyACM0`, the bridge driver's sysfs files, the USB sound card). The app talks to it on 127.0.0.1: 9980 for commands, 9985 for audio, each message behind a 12-byte header | read |
| Bridge MCU | STM32, USB `0483:5730` (CDC-ACM plus USB Audio), build `20181221151755`; the same bridge family as the Atom XL's | report, read |
| Wire protocol | the Agold envelope `7E 96 69 … 81`, as on the Atom XL. Inside it, an **older command set**: `0x35` analog channel (15 bytes), `0x36` digital channel (156 bytes, **no time slot**, IDs big-endian), `0x25` version, `0x02` volume, `0x07` text send, `0x11` text fetch, `0x10` call info, `0x04` reception start/end push | read, report |
| Module version string | `ver0.5.4_470M_TONE` (reply to `0x25`) | report |
| Module chip | unknown: no image, and the version string is not in the `DMR00x` format of the HR-C7000 family | — |
| Keying | the daemon's PTT control: the bridge's PTT line plus a bridge frame. The module gets no key command | read |
| Audio | 48 kHz stereo 16-bit, 10 ms frames, over the daemon's socket (32 kHz with `ro.agold.extmodule.32k`) | read |
| Frequencies | the intercom app accepts 100–470 MHz. The module's own range is not measured; the owner listens at 133.85 MHz | read, owner |
| Side key | scancode `0xf9` on `mtk-kpd` | report |

**Loader:** the daemon has a module update path (YModem after a PTT-held start, the same scheme as the Armor 26 Ultra's knock). But **no module image exists**: two stock ROMs a year apart and the owner's Magisk module carry only the bridge MCU's images. The module has no flash read command that we know of. The tester asked for no firmware changes, and SignalDeck's loader is off for this phone (uncertified).

**Stock image:** none. No image is offered to this phone.

Full findings: phonedmrapp `docs/multi-device-armor3wt-findings.md` and `docs/armor3wt/stock-app-review.md`.
