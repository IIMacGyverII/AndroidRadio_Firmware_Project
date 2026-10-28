# Unihertz Atom XL

**Status: report + read + bench, unverified.** From two owner device reports (2026-10-24), the stock app
`com.agold.intercom` v2.0 decompiled offline, and a bench phone (from 2026-10-28; read only and identity queries so
far, full notes in `phonedmrapp/docs/atomxl/PHASE_A_FINDINGS.md`).

| Item | Value | Source |
|---|---|---|
| SoC | MediaTek MT6771 (Helio P60), Android 11 | report |
| ODM | Agold (`com.agold.*`, `com.agui.*`) | read |
| Module version string | **varies per unit:** `DMR006.U4A.V082` on the reporting owner's phone, `DMR006.U4A.V067` on the bench phone (HR-C7000 family) | report; measured |
| Bridge MCU | STM32, USB `0483:5730` "Agold Audio Class" (USB Audio + CDC-ACM); route `00` cmd `0x01` answers its build date (`20201016161541` on the bench phone, one of the five images in `/vendor/data/mcu/`) | measured |
| Transport | vendor HAL `vendor.mediatek.hardware.aguiextmodule@1.0` holding `/dev/ttyACM0` (USB CDC-ACM to a small MCU in front of the module) | read |
| Frame format | `7E 96 69 | route | cmd | rw | len (BE) | body | checksum (BE) | 81`; route `00` = the MCU, `01` = passed to the module; Internet checksum over route…body | read |
| Command set | the Armor's command bytes inside that envelope (`0x34` version, `0x23`/`0x24`/`0x25` channels, `0x2C` texts with a 5-byte header where the Armor's firmware needs 9) | read |
| Audio | on the wire: USB Audio card 1 (`pcmC1D0c`/`pcmC1D0p`), **32 kHz** stereo S16, opened by the HAL; the stock app's side is 48 kHz stereo through the HAL (`openPcmIn/Out`, `readPcmDevice`, `writePcmDevice`) | measured; read |
| USB | **radio on = no USB to a PC:** powering the radio switches the phone's only USB controller to host mode for the bridge, so a PC link (adb, file transfer) drops and comes back only after a reboot: force-stopping the stock app does not power the radio off, and even its clean power-off (HAL `stopMcu`) leaves the controller in mode "none", replug or not | measured |
| PTT key | `mtk-kpd` key code 249 → `FUNC1` → Android keycode 289 (a vendor keycode), press-tested; the stock app receives it as `android.intent.action.PTT.down` / `.up` | measured; read |
| Loader | HAL methods `updateMcu` and `updateDmr`; how they reach the module is not captured | read |
| Default frequencies in the stock app | UHF around 401 MHz, one analog at 444.800 MHz | read |

**The running image is not on the phone** (bench phone, searched read only 2026-10-28): the vendor partition holds
only V076, the stock APK no image, the HAL's second update folder (`/storage/self/primary/intercom/dmr/`) does not
exist, and a string search of every partition except `userdata` finds no other image (the only other hit is a list of
version names, V067/V076/V080/V082, in a factory-test app). Since the module's version differs between units, a port
needs the image of the unit it is built for, from a source other than the phone: nothing reads a module's flash on
this phone yet.

**What a port needs first:** a capture of one stock-app update to learn how `updateDmr` enters the module's update
mode through the MCU (the HAL sends YModem through the bridge; owner's decision), and the module image the unit runs
(V067 or V082). The stock APK carries no image; the phone keeps an older one, `DMR006.U4A.V076`,
on its vendor partition (`/vendor/data/DMR/dmr/`), now in `firmware/unihertz-atom-xl/DMR006.U4A.V076/` for research
(not a restore image). A different build from the Armor's, so its own patch set. V076's command dispatch,
`0x3B` and `0x34` handlers are read (the Armor's jump-table switch, a different case epilogue; offsets in the
image's README); they are V076's, not V082's, so nothing is built for this phone from them. Full findings: `phonedmrapp/docs/multi-device-atomxl-findings.md`.
