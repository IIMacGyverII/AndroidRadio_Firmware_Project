# HR-C7000 + AT1846S

The DMR/FM module inside the Ulefone Armor 26 Ultra and, by version string and protocol, its relatives. Facts below
are from the Armor's stock image `DMR003.UV4T.V022` unless marked; another build (the Atom XL's `DMR006.U4A.V082`)
needs its own addresses, which `phonedmrapp/tools/fw-port/find_symbols.py` proposes from the image.

## Hardware

| Item | Fact |
|---|---|
| Core | HR-C7000 SoC, **C-SKY V2** instruction set (T-Head); not ARM. Disassemble with `csky-elfabiv2-objdump` or the Ghidra C-SKY module |
| Image | 378,620 B, plaintext, no signature; executes in place from flash at `0x0301A000`; IRAM copied from file `+0x39408`, SRAM from `+0x322E0`; the version string sits at file offset `0x38464` (16 bytes) |
| Bootloader | below the image in flash (the image starts `0x1A000` into it); it answers the update prompt and is not written by a load |
| RF IC | AT1846S over I²C (write routine file `+0x54628`, read `+0x54664`); register `0x58` holds the voice filters: `0x8405` all on (analog), `0xBCFD` all bypassed (DMR) |
| Modem RAM | TX RAM at `0x16000000` (two 256-sample halves, 8 kHz), FM receive RAM mirror at `0x160004E0` |
| Audio | the module's own codec is not in the phone's audio path on the Armor; converters are phone-side |

## Protocol (UART, 57600 on the Armor)

Frames `68 … 10`; dispatcher at file `+0xAA3C`, table at `+0x38240` indexed by `cmd − 0x22`. Command `0x40` is a
free slot in the stock image (empty handler) and is where every modified image puts its extensions; `0x3D` has a
real handler nobody uses. `0x34` returns the version string. `0x3B` stores the transmit time-out byte (seconds):
**0 turns the timer off**, the firmware's own start-up value is 120, there is no clamp. Status bytes: 3 send
start, 4 send stop, 1/2 receive start/stop; the time-out expiry sends 4.

## Update mode and loader (measured on the Armor, 2026-10-25)

There is no "enter bootloader" command. The stock updater power-cycles the module with PTT held (`pwd` low, 50 ms,
`ptt` low, 50 ms, `pwd` high, 1000 ms, `ptt` high), writes the byte `0x31`, and the module answers `C`. Then plain
YModem-1K: SOH block 0 (name, NUL, decimal size), `ACK` then `C`, STX 1024-byte blocks with sequence, complement and
CRC-16-CCITT (init 0), `EOT`, a zero end block, one `ACK`. 15 s per block, six retries, `NAK` resends, `CAN` aborts.
No MD5, no signature. The erase takes about 11.4 s after the header; blocks are acknowledged in about 0.29 s. A
transfer killed half way leaves the bootloader intact; the knock then works again. **Nothing in the stock image
returns flash**; images from this project add opcode 12 (file offset + length ≤ 240) for read-back.

## What the modified images add (FW19–FW22 on the Armor; bench images, kept in phonedmrapp until released)

- A symbol engine on command `0x40`: a 2048-symbol ring, RRC shaping, playback through the DMR modulator from
  TX RAM (M17 proven: 1125 of 1125 frames), a self-unkey that waits for the shaping buffers, runs the stock unkey
  while the module still believes it is transmitting (otherwise the receiver stays off), then clears the time-out
  state.
- Generic engines: 2- or 4-level symbols at a rational rate with a hold or polyphase pulse; a 64-pair
  phase-continuous tone queue in eighths of a hertz (POCSAG 1200, MCW, RTTY 45.45 and FT8 all decoded).
- A receive filter hold (AT1846S `0x58` = `0xBCFD`) that makes the phone's receive audio flat for data modes.
- The time-out floor: a `0x3B` byte of 0 or above 120 becomes 120.
- Opcode 12 flash read.

None of them touch band limits or power, and none keys at boot.

## Measured limits worth knowing

- Tuning range enforced by the module: 136.000–174.000 and 400.000–480.000 MHz, 500 Hz steps.
- The DMR modulator path compresses near ±4.1 kHz deviation on the Armor at low power.
- A 120 s high-power key heats the Armor's AP thermal zone by about 11 °C; the module's own limit is the 120 s default.

Sources: `phonedmrapp/docs/deep-dive/19-firmware-modification-plan.md`, `docs/grok-deep-dive/11-firmware-fw0-results.md`,
`radio_firmware/results.md`, `radio_firmware/reviews.md`, `radio_firmware/symbols.csv`.
