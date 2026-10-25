# Ulefone Armor 3WT

**Status: report + read, unverified.** From one owner's SignalDeck device report (2026-10-25) and the intercom app
it contained (`com.agold.intercom` v2.0, an older build of the Atom XL's). The phone in that report runs a LineageOS
GSI with the vendor programs supplied through the owner's own Magisk module. Nothing has been run on a 3WT by us.

| Item | Value | Source |
|---|---|---|
| SoC / board | MediaTek MT6771, board `s62v71c2k_gq_3wt`, kernel 4.4 | report |
| ODM family | Agold, the same as the Unihertz Atom XL | read |
| Transport | two local sockets to a daemon that owns a USB MCU in front of the module | read |
| Module | HR-C7000 family behind the MCU | inferred |
| Loader | not captured; the Atom XL's HAL has `updateDmr`, this build's daemon is expected to have the equivalent | inferred |

Full findings: `phonedmrapp/docs/multi-device-armor3wt-findings.md`. No image is offered to this phone.
