# Blackview Xplore 1

**Status: read, unverified.** From the stock walkie-talkie app `QuickChatEEA.apk` (`com.chamsion.quickchat`,
"InterPhone", V1.0), analysed offline in 2026-10, plus owner dumps from 2026-10-21. Nothing has been run on an
Xplore 1 by us. SignalDeck profile id `blackview-xplore1` (unverified).

| Item | Value | Source |
|---|---|---|
| Phone | DokeOS 5 / Android 15, MediaTek Dimensity 7050 | read |
| Radio SDK in the app | `com.wonder.dmr` + `com.wonder.serial` (JNI serial port library) | read |
| Protocol | the same module command family as the Armor (verified from the code, 2026-10-17) | read |
| Differences | audio as PCM over `/dev/ttyS1`; sysfs node names differ | read |
| Loader | not captured; expected to be the module's YModem bootloader behind a similar knock | inferred |
| Stock image | not yet extracted | |

Full findings: `phonedmrapp/docs/multi-device-xplore1-findings.md`. No image is offered to this phone.
