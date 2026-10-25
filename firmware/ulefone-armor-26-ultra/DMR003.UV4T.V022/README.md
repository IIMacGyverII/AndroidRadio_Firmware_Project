# DMR003.UV4T.V022 — the Armor 26 Ultra's stock module firmware

The factory image. Loading it puts the module back exactly as the phone shipped. It is the restore target for every
other image for this device, and the base every modified image is built on.

| Item | Value |
|---|---|
| File | `DMR003.UV4T.V022.bin`, 378,620 bytes |
| SHA-256 | `90e361fda1082cdd010f8f2127eab97786f2a078f2f7590821c26867526c8c10` |
| MD5 | `4426035392262ca54583c230c9e268e0` |
| Taken from | the stock app `com.pri.prizeinterphone` V1.0, `assets/DMR003.UV4T.V022.bin`, byte for byte |
| Version string | `DMR003.UV4T.V022` at file offset `0x38464` |
| Transmit time-out | the firmware's own start-up value is 120 s; the stock app sends 0 at start, which turns the module's timer off (the stock app then limits keys itself) |
| Persists | yes, across reboots and module power-cycles, until another image is loaded |
| Read-back | no; the stock image has no command that returns flash |

SignalDeck extracts this same asset from the stock app on the user's phone, checks it against this hash and keeps it
as the backup before any other image is loaded. If the stock app is gone, this file is the copy the catalogue offers.

Research on this image: `phonedmrapp/docs/grok-deep-dive/11-firmware-fw0-results.md` (first analysis, 2026-10),
`phonedmrapp/docs/deep-dive/19-firmware-modification-plan.md` (the plan built on it), `phonedmrapp/radio_firmware/symbols.csv`.
