# ANYSECU W6+

**Status:** measured on a bench unit (2026-10-27), plus the stock app read offline. Analog UHF only; **no DMR**. A
different module family from every other phone here: an SA818-class AT-command module, not the HR-C7000.

## Phone

| Item | Value | Source |
|---|---|---|
| SoC, Android version, build | Unisoc SL8541E (`sp9832e`), Android 12, 32-bit only, kernel 5.4; `Build.MODEL` `W6+` | measured |
| Stock radio app | `com.flyscale.analogpoc` (`/system/priv-app/FlyscaleAnalog400/`, system uid, shared user `android.uid.system`) | measured / read |
| Stock firmware asset | none: the stock app carries no module image and has no update path | read |
| Module control | `/dev/ttyS2`, 9600 8N1 raw (SELinux label `console_device`), opened by the stock app's `libserial_port.so` (`android.serialport.SerialPort`) | measured (serial sniff) / read |
| Module power / PTT | power `gpio322` (1 on, 0 off); transmit `gpio188`, mic to the module `gpio222` (`gpio179` picks the headset mic); receive detect `gpio189` (an input, 1 while the squelch is open) | read (stock app code) / measured (power, receive detect) |
| Audio | received audio goes from the module to the speaker amplifier through hardware switches (`gpio183` speaker route, `/sys/kernel/ext_pa_en`, `/sys/kernel/dmr_state` 1 while receiving); Android records the same audio on the **camcorder** input while those are set | measured (HackRF in a shielded enclosure) |
| Side PTT key | input device `hook_dmr` (`KEY_F2`, `KEY_F3`), broadcasts `fly.privkey.poc.down/up/long` | measured / read |
| Root | Magisk; SELinux is permissive on this build. SignalDeck's sepolicy lines for the port: `console_device` | measured |

**Never read an attribute of `/sys/devices/virtual/misc/flyscale_misc/`.** `af_en` and `dmr_pwd` there each panicked
the kernel when read (their show handlers touch GPIOs this board does not have). The GPIO numbers above are the ones
the stock app actually uses.

## Module

SA818 family, `../../modules/sa818-class-pb202/`. Version `PB202EU05` (`AT+DMOVERQ`). Nothing sits between the phone
and the module: the app writes text commands straight to the UART.

## Update mode

None known. The stock app has no firmware asset, no update command and no update screen; the module answers only its
documented `AT+DMO…` commands (unknown input comes back as an error echo ending `:1`). Reading the module's firmware
needs physical access to the module's MCU (its programming interface on the module board), which has not been done.
**No image is offered to this phone, and none can be dumped from software.**

## What is known not to be in software

- **Receive audio cut below ~300 Hz** (measured 2026-10-27, HackRF FM tones at ±1.5 kHz deviation, recorded through
  the camcorder input; relative to 1 kHz): 62.5 Hz absent, 125–187.5 Hz −57 dB, 250 Hz −48 dB, 312.5 Hz +12.5 dB;
  above that the expected de-emphasis slope (about −6 dB per octave, 500 Hz +8.6 dB to 4 kHz −21.5 dB). The cut is
  steeper than the HR-C7000 phones' (−25 to −37 dB there).
- **The filter command is not accepted:** `AT+SETFILTER=1,1,1` and `AT+DMOSETFILTER=1,1,1` both came back as error
  echoes, so the high-pass cannot be bypassed over the UART. Data modes that need the bottom octave (M17's lowest
  symbol energy, POCSAG's DC content) inherit the same problem as on the HR-C7000 phones, without the firmware route.
- **No signal-strength reading:** `RSSI?` is not answered.
- Range: 400–470 MHz per the listing; the module's own limits are not measured.

## Images for this device

None.

## Sources

`SignalDeck` `docs/w6/` (device report findings, serial sniff, engine design, receive-audio test) and the SignalDeck
`ANYSECU_W6` profile (`anysecu-w6plus`, unverified: transmit is not tested on air).
