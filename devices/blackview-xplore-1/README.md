# Blackview Xplore 1

**Status: report + read, unverified.** Sources:
- the stock walkie-talkie app `QuickChatEEA.apk` (`com.chamsion.quickchat`, "InterPhone", V1.0, protocol library `com.wonder.dmr` 1.0.9), first analysed offline 2026-10-17/22 and **read line by line, transmit first, on 2026-10-30** (phonedmrapp `docs/xplore1/stock-app-review.md`);
- owner dumps (2026-10-21) and a tester's SignalDeck device reports (beta.1–18, 2026-10-21 to 24): receive, MON, CTCSS and the module restart work.

Nothing has been transmitted on an Xplore 1 by us. SignalDeck profile id `blackview-xplore1` (revision 3, unverified).

| Item | Value | Source |
|---|---|---|
| Phone | DokeOS 5 / Android 15, MediaTek Dimensity 7050 (`mt6877`), model `XPLORE 1 Walkie Talkie` | report |
| Radio SDK in the app | `com.wonder.dmr` + `com.wonder.serial` (`libwonder_serialport.so`), `me.f1reking.serialportlib` for the audio port; both libraries are in the APK, none on `/system` | read, report |
| Wire protocol | the Armor's `68 … 10` frames, the same checksum, the same command numbers and body layouts (`0x22` 163 B, `0x23` 19 B) | read |
| Module version | `DMR003BN.UV4P.V016` | report |
| Module control | UART `/dev/ttyS0` at 57600 | read, report |
| Audio | **PCM over `/dev/ttyS1` at 230400 8N1**. Receive: 167-byte packets `BB 00 00 A0 xx xx` + 160 B + `44` (8 kHz mono 16-bit LE, 10 ms each, 100 packets/s while the squelch is open). Transmit: raw 160-byte blocks, no header, at least 10 ms apart | read, report (receive) |
| Lines | `/sys/devices/platform/intercom/intercom_{power,pwd,ptt}_control` (plain `sysfs`, mode 0777, write-only). Power-up: power, pwd, ptt `1`; power-off: all `0` | read, report |
| **Keying** | **`intercom_ptt_control` `0` = transmit, `1` = receive. The stock app never sends `0x26`.** It opens the microphone when the module reports SEND_START (status 3) and stops it 200 ms after the line goes back to 1 | read |
| Side key | `com.android.intent.ptt.down/up` (input `KEY_F1`); the app refuses a key within 1.5 s of the last release | read, report |
| Boot handshake | banner → `0x27` → `0x34` → channel; after each channel's acknowledgement `0x35` 2 → `0x37` 0, and for analog `0x2F` + `0x30` 200 ms later. Never `0x2A`, `0x2B`, `0x31`, `0x32`, `0x3C`; `0x3B` only when the user changes the transmit limit; `0x36` never acknowledged | read |
| Texts | `0x2C` body = type (1/2 private, 3 group), target LE32, **UTF-8** text (5-byte header); received texts read as UTF-8 | read |

**Loader** (read): the app has a hidden firmware-update screen (secret code `*#*#18233#*#*`):
1. The knock: ptt line `0`, 55 ms later power + pwd `1`, 1050 ms later the ptt line back to `1`.
2. The byte `0x31`.
3. YModem-1K with CRC16-XMODEM (`01` header packet "Filename.bin" + size, `02` 1 KiB packets, `04` at the end).

This is the same family as the Armor 26 Ultra's update mode. The user picks the image file; **the APK carries no image**.

**Stock image:** not extracted. The variant `DMR003BN.UV4P.V016` has never been diffed against the Armor's `DMR003.UV4T`. Under the loader safety contract **no image is offered to this phone**, and SignalDeck's loader is off for this profile.

Full findings: `phonedmrapp/docs/multi-device-xplore1-findings.md` and `phonedmrapp/docs/xplore1/stock-app-review.md`.
