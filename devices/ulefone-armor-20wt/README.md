# Ulefone Armor 20WT

**Status: report + read, unverified.** From one owner's SignalDeck device report (2026-10-24) and its stock app,
the same PriInterPhone family as the Armor 26 Ultra. Nothing has been run on a 20WT by us. SignalDeck profile id
`ulefone-armor20wt` (unverified).

| Item | Value | Source |
|---|---|---|
| Stock radio app | `com.pri.prizeinterphone` family, same command table | report, read |
| Module control | UART `/dev/ttyS1` at 57600 (`ttyS0` is another device on this phone) | read |
| Serial library | `libserial_port_app.so` in the stock app's own folder, bound to `com.serial.port.SerialPort` | read |
| Power / PTT nodes | `dmr009` `pwd` / `ptt`, as on the 26 Ultra | read |
| Side key | keycode 301 with `com.interphone.ptt.down/up` | report |
| Audio | PrizeTinyService, as on the 26 Ultra | read |
| Module version string | not yet seen (the module was powered off during the report's probe) | report |

**Loader:** expected to be the same GPIO knock and YModem path as the 26 Ultra; not captured. **Stock image:** not
yet extracted. No image is offered to this phone until both are known and the stock asset is in this repository.
