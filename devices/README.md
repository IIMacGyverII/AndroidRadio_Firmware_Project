# Devices

One folder per phone, named `<vendor>-<model>` in lower case with hyphens. Each has a `README.md` for people and a
`device.json` with the same facts for scripts. Every fact says where it came from: **measured** (run on the phone by
us), **report** (a SignalDeck device report from an owner), **read** (the stock app's code or the firmware image,
read offline), or **inferred**.

| Folder | Phone | Module version string | Transport to the module | Status |
|---|---|---|---|---|
| `ulefone-armor-26-ultra` | Ulefone Armor 26 Ultra | `DMR003.UV4T.V022` | UART `/dev/ttyS0` 57600, GPIO `dmr009` | measured; loader proven 2026-10-25 |
| `ulefone-armor-20wt` | Ulefone Armor 20WT | same family (PriInterPhone) | UART `/dev/ttyS1` 57600, GPIO `dmr009` | report + read; unverified |
| `ulefone-armor-3wt` | Ulefone Armor 3WT | HR-C7000 family | local sockets to a daemon owning a USB MCU | report + read; unverified |
| `unihertz-atom-xl` | Unihertz Atom XL | `DMR006.U4A.V082` | vendor HAL, USB CDC-ACM `/dev/ttyACM0`, framed envelope | report + read; unverified |
| `blackview-xplore-1` | Blackview Xplore 1 | same protocol family | UART, audio as PCM over `/dev/ttyS1` | read; unverified |
| `doogee-s80` | DOOGEE S80 | sibling protocol (`DMR007`) | UART | read; unverified |

A device page is the first thing a port needs; the loader path and the stock firmware asset are the two facts that
decide whether an image can ever be offered there (`../SAFETY.md`).
