# Ulefone Armor 26 Ultra

The reference phone. Everything in this repository was first measured here. SignalDeck profile id
`ulefone-armor26ultra`.

## Phone

| Item | Value | Source |
|---|---|---|
| Stock radio app | `com.pri.prizeinterphone` (PriInterPhone), versionName `V1.0`; a privileged app | measured |
| Stock firmware asset | `assets/DMR003.UV4T.V022.bin` inside that APK (378,620 B, SHA-256 `90e361fd…c8c10`); the stock updater also accepts `/sdcard/DMR/DMRDEBUG.bin` as an override | read, measured |
| Module control | UART `/dev/ttyS0` at 57600, opened through the stock app's own serial JNI library (`/system/lib64/libinterphone_serial_port.so`); `stty` cannot set this port's speed | measured |
| Module power / PTT | sysfs `/sys/devices/platform/dmr009/pwd` and `/sys/devices/platform/dmr009/ptt` | measured |
| Audio | 8 kHz stereo-duplicated PCM through `PrizeTinyService` (phone-side ES8311 codec at 8 kHz; the module's own codec is not in the path) | measured |
| Side PTT key | `android.intent.action.PTT.down/up` (keycode 381); `com.interphone.ptt.down/up` when assigned to the stock app | measured |
| Root | Magisk; four sepolicy rules (the `ttyS` device and the `sysfs_prizefactory` nodes for an untrusted app) | measured |

## Module

HR-C7000 (C-SKY V2) with an AT1846S RF IC; see `../../modules/hr-c7000/README.md`. Version string `DMR003.UV4T.V022`.

## Update mode (measured 2026-10-25)

Power-cycle through the GPIOs with PTT held: `pwd` low, 50 ms, `ptt` low, 50 ms, `pwd` high, 1000 ms, `ptt` high;
write the byte `0x31`; the bootloader answers `C` about 200 ms later and takes plain YModem-1K (no MD5, no
signature). Erase about 11.4 s after the header, 1 KiB blocks acknowledged in about 0.29 s each, a power-cycle and
the version query afterwards. SignalDeck's own sender did five proof loads including recovery after a transfer
killed half way. Detail: `phonedmrapp/radio_firmware/plan-loader-safety.md` and `results.md`.

## What is known not to be in software

The tuning range (136–174 / 400–480 MHz) is enforced by the module; the transmit path's cut below ~250 Hz is on the
phone side (ES8311) and cannot be opened by module firmware; a 144.770 MHz high-power key can reset the phone's USB
port (cable pickup). Details and dates: `phonedmrapp/CLAUDE.md` §3 and the deep dives.

## Images for this device

`../../firmware/ulefone-armor-26-ultra/`: the stock image; released images built on it are added when the owner releases them (bench images stay in phonedmrapp).
