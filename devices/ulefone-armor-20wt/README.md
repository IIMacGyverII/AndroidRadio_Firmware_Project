# Ulefone Armor 20WT

**Status: report + read, unverified.** Sources:
- one owner's SignalDeck device report (2026-10-24);
- a line-by-line reading of its stock app against the Armor 26 Ultra's (2026-10-30; phonedmrapp `docs/armor20wt/stock-app-review.md`).

Nothing has been run on a 20WT by us. SignalDeck profile id `ulefone-armor20wt` (revision 2, unverified).

| Item | Value | Source |
|---|---|---|
| Stock radio app | `com.pri.prizeinterphone` `V1.0` (versionCode 31): an older build of the Armor 26 Ultra's app. No command state machine, no firmware updater, no `DMR*.bin` asset, no native libs in the APK | read |
| Wire protocol | `68 … 10` frames, the same checksum, the `BF AA` boot banner; the same command numbers and status codes. Every message body has the same layout; the one difference is the default analog volume byte (5 here, 8 on the 26 Ultra). The 26 Ultra's `0x3F` bit-error test is absent | read |
| Commands the stock app sends | `0x22`, `0x23`, `0x26`, `0x27`, `0x2C`, `0x2D`, `0x34`, `0x3B`, `0x36` acks. Whether the module implements the others (`0x32` RSSI, `0x2B` caller info, `0x2F` monitor, `0x30` squelch …) is unknown | read |
| Boot handshake | banner → channel → `0x34`; `0x3B` 0 after the version reply; `0x27` at 6 s with no banner | read |
| Module control | UART `/dev/ttyS1` at 57600 (`ttyS0` is another device on this phone) | read |
| Serial library | `libserial_port_app.so` in `/system/priv-app/PriInterPhone/lib/arm64/`, bound to `com.serial.port.SerialPort` | read, report |
| Power / PTT nodes | `dmr009` `pwd` (power: written 1 at start, 0 on exit). `ptt` exists (`ptt :1` at rest) but **the stock app never writes it**; keying is UART `0x26` only | read, report |
| Side key | keycode 301 (`smartlinkkey`), sent as `com.interphone.ptt.down/up` (each broadcast twice per press) | report |
| Audio | PrizeTinyService, 8 kHz stereo 16-bit both ways. The microphone path opens 600 ms before `0x26` 1; receive opens at each `RECEIVE_START` | read |
| Module version string | not yet seen (the module was powered off during the report's probe) | report |

**Loader:** the stock app has **no update path**. There's no YModem code, no knock, and it never touches the `ptt` line. Whether this module's bootloader answers the 26 Ultra's knock is therefore unknown, and SignalDeck's loader is switched off for this profile.

**Stock image:** the APK carries none, so it can only come from the phone (SignalDeck *Device → Device report → Radio firmware files* lists name, size and SHA-256). No image is offered to this phone until the variant is known and its stock copy is in this repository.
