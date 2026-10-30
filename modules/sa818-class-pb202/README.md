# SA818-class analog module (PB202EU05)

An analog FM transceiver module driven by text commands over a UART, in the family of the SA818/SA868 modules.
Found in the ANYSECU W6+ (UHF, 400–470 MHz). Version string `PB202EU05` (`AT+DMOVERQ`). The chip inside is not
identified (the module has not been opened). Facts below are measured on one bench unit (2026-10-27) unless marked.

## Interface

- UART 9600 8N1, raw. Commands are ASCII ending in a **bare CR** (no LF), one command per write; the stock app leaves
  about 100 ms between commands and waits for each answer.
- Answers are `\r\n+DMO<NAME>:<value>\r\n`; `:0` = done, `:1` = refused. **Input the module does not understand comes
  back as an error echo** (the received text, sometimes missing a byte, followed by `:1`), including binary frames.

## Commands the stock app uses (read from its code, sniffed on the wire)

| Command | Arguments | Answer |
|---|---|---|
| `AT+DMOCONNECT` | none; the stock app repeats it once a second until answered | `+DMOCONNECT:0` |
| `AT+DMOVERQ` | none | `+DMOVERQ:PB202EU05` |
| `AT+DMOSETGROUP=gbw,tx,rx,txTone,rxTone,sq,power` | gbw 0 = 12.5 kHz, 1 = 25 kHz; frequencies in MHz (`435.025`); tone code; squelch 0–8 (0 = monitor); power 0 low, 1 high. **Transmit tone before receive tone, then squelch, then power**: a different order from the public SA818 manual | `+DMOSETGROUP:0` / `:1` |
| `AT+DMOSETVOLUME=n` | 0–8 | `+DMOSETVOLUME:0` |
| `AT+DMOSETMIC=…` | 1–8 per the stock app's settings list; the argument format was never seen on the wire | — |
| `AT+DMOSETVOX=n` | 0 off, 1–8 | (read) |
| `AT+DMOAUTOPOWCONTR=n` | power saving 0 off, 1–16 | (read) |

Tone codes (from the stock app's resource arrays): 0 none; 1–38 the standard CTCSS tones 67.0–250.3 Hz; 240–252 the
other 13 (240 = 62.5, 241 = 69.3, 242 = 159.8, 243 = 165.5, 244 = 171.3, 245 = 177.3, 246 = 183.5, 247 = 189.9,
248 = 196.6, 249 = 199.5, 250 = 206.5, 251 = 229.1, 252 = 254.1 Hz); 39–121 the 83 DCS codes 023N–754N (normal
polarity only).

## Not available (tried)

- `RSSI?`: no answer (six tries, with and without a signal).
- `AT+SETFILTER=1,1,1` and `AT+DMOSETFILTER=1,1,1`: error echoes. The receive high-pass (below ~300 Hz, see the
  device page for the measured response) cannot be bypassed this way.
- No firmware read or update command is known; the module's firmware has not been dumped. Doing so needs physical
  access to its MCU's programming interface.

## Lines around the module (the W6's wiring)

Power, transmit, microphone, receive-detect and audio-route GPIOs are per phone: see
`../../devices/anysecu-w6plus/README.md`.
