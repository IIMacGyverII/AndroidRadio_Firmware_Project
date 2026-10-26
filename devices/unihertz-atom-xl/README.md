# Unihertz Atom XL

**Status: report + read, unverified.** From two owner device reports (2026-10-24) and the stock app
`com.agold.intercom` v2.0, decompiled offline. Nothing has been run on an Atom XL by us.

| Item | Value | Source |
|---|---|---|
| SoC | MediaTek MT6771 (Helio P60), Android 11 | report |
| ODM | Agold (`com.agold.*`, `com.agui.*`) | read |
| Module version string | `DMR006.U4A.V082` (HR-C7000 family; the phone-side MCU reports its own build date) | report |
| Transport | vendor HAL `vendor.mediatek.hardware.aguiextmodule@1.0` holding `/dev/ttyACM0` (USB CDC-ACM to a small MCU in front of the module) | read |
| Frame format | `7E 96 69 | route | cmd | rw | len (BE) | body | checksum (BE) | 81`; route `00` = the MCU, `01` = passed to the module; Internet checksum over route…body | read |
| Command set | the Armor's command bytes inside that envelope (`0x34` version, `0x23`/`0x24`/`0x25` channels, `0x2C` texts with a 5-byte header where the Armor's firmware needs 9) | read |
| Audio | 48 kHz stereo 16-bit PCM through the HAL (`openPcmIn/Out`, `readPcmDevice`, `writePcmDevice`) | read |
| Loader | HAL methods `updateMcu` and `updateDmr`; how they reach the module is not captured | read |
| Default frequencies in the stock app | UHF around 401 MHz, one analog at 444.800 MHz | read |

**What a port needs first:** a capture of one stock-app update to learn how `updateDmr` enters the module's update
mode through the MCU, and the module image it runs (V082). The stock APK carries no image; the phone keeps an older one, `DMR006.U4A.V076`,
on its vendor partition (`/vendor/data/DMR/dmr/`), now in `firmware/unihertz-atom-xl/DMR006.U4A.V076/` for research
(not a restore image). A different build from the Armor's, so its own patch set. Full findings: `phonedmrapp/docs/multi-device-atomxl-findings.md`.
