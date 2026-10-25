# <Vendor Model>

**Status:** report + read, unverified | measured. Say which, per fact, in the Source column. Nothing that identifies
the reporting owner goes in this file.

## Phone

| Item | Value | Source |
|---|---|---|
| SoC, Android version, build | | report |
| Stock radio app | package, versionName, whether it is a privileged app | report / read |
| Stock firmware asset | path inside the APK, size, SHA-256; the updater's override path if any | read |
| Module control | serial device and baud, or HAL/socket; the serial library it uses | read / measured |
| Module power / PTT | sysfs nodes, or the MCU command | read / measured |
| Audio | path (TinyService, UART PCM, HAL), sample rate and format | read / measured |
| Side PTT key | keycode and broadcast | report |
| Root | what the app needs (sepolicy lines, Magisk) | measured |

## Module

Family (`../../modules/…`), version string(s) returned by `0x34`, anything the phone's build adds in front of
the module (an MCU, a daemon).

## Update mode

How the stock app enters it (GPIO knock, HAL method, MCU command), the prompt byte, the protocol, and whether a
capture of one stock update exists. Until this is captured: "not captured; no image is offered to this phone".

## What is known not to be in software

Range limits, audio-path cuts, anything hardware.

## Images for this device

Link to `../../firmware/<device>/` once a stock image is there; otherwise say "none".

---

Also fill `device.json` (schema: `../device.schema.json`) and `variants.json` (format: `../VARIANTS.md`).
