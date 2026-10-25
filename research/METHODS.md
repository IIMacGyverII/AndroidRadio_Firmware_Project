# Methods: how the firmware was understood, changed and tested

Everything in this repository was produced by one bench, one reference phone, two AI agents and a review loop.
This page says how, so that a result can be repeated and a new phone can be worked the same way. The detailed
procedures and every measurement are in phonedmrapp (`radio_firmware/results.md`, `reviews.md`, ch. 19).

## 1. The bench

- **Inside a shielded enclosure.** The phone, the radio module and a HackRF One sit together in a Faraday cage,
  so every key and every capture stays off the air. The HackRF never transmits from the outdoor antenna.
- **Phone over Wi-Fi ADB; HackRF on the bench PC.** Scripts drive both: SignalDeck's diagnostics receiver on the
  phone (hidden bench extras behind a Diagnostics flag), `hackrf_transfer` on the PC.
- **Defaults for comparability:** 467.625 MHz, low power, so numbers compare across images. Other frequencies and
  powers are used when a test needs them and are stated in the result.
- **Equipment-protection rules, not regulatory ones:** HackRF receive gain kept out of clipping (the clip fraction
  is reported with every capture), a dummy burst before the first HackRF transmission after a pause, never a
  backgrounded capture, heat rules (below), and only the documented YModem path into the module.

## 2. Reading the firmware

- The image is **C-SKY V2** (T-Head), not ARM: `csky-elfabiv2-objdump` and a Ghidra C-SKY module. The first
  analysis (memory map, dispatcher, I²C driver, channel handlers) is `phonedmrapp/docs/grok-deep-dive/11-…`.
- **Named addresses** go into `radio_firmware/symbols.csv`; every patch site in `tools/fw-patch/patches.toml`
  records the original bytes, so a build refuses an image whose bytes are not what the patch expects.
- **Anchors, not addresses, for the next phone:** `tools/fw-port/find_symbols.py` finds the version string, the
  dispatch entries, the time-out timer and the free stub space in any image of the family by their patterns.
- **The stock app is read offline** (decompiled) to learn handshakes and layouts; our implementations are then
  written from the standard or from what the wire showed, not copied.

## 3. Building an image

- `tools/fw-patch/build.py`: factory image + named patches → a tagged image + its SHA-256. The tag is written into
  the version string, so `0x34` always says what is in the module. `check.py` attributes every changed byte to a
  patch or the tag and fails on anything unattributed.
- Stubs are small assembly routines in the free flash slot (`+0x5AEFC` on the Armor); the stock command handler
  `0x40` is the entry point, so no stock handler is replaced.
- **Rule: nothing keys at boot.** Every stub acts only on a host-requested transmission.
- **Rule: no band-limit or power patches, ever.**

## 4. Testing an image

The order is fixed and the same for every image:

1. **Host tests first.** Patch-table tests (`test_patches.py`), encoder tests against the research implementation,
   and for the loader a sender test with a fake wire. Nothing is loaded until they pass.
2. **Render before key.** Any waveform-path change is rendered inside the module (op 4 returns samples without
   keying) and compared with the expected samples before the first key. The one build that was wrong hung on a
   render, not on the air.
3. **Load, tag, boot capture.** The image is loaded, `0x34` must return its tag, and a HackRF capture across the
   module's boot must stay under the radiation threshold (0.1 dB peak against a 10 dB stop).
4. **Keys with pass criteria written before the run.** Each step's handoff names the measurement and the number
   that passes (frames decoded, deviation, timing, status bytes). The HackRF capture is analysed for carrier
   length, clip fraction, body deviation (p99 of the FM instantaneous frequency, first and last 50 ms dropped),
   and a ±5 kHz stop that ends the step if any slice reaches it.
5. **Decode with our own decoders, payload-exact.** The measure for a digital mode is the number of frames whose
   payload bytes equal what was sent, never "sync found" or a raw bit-error estimate. M17 and POCSAG decoders
   are ours (`tools/m17-research`, `tools/pocsag-research`); RTTY and FT8 use SignalDeck's own decoders on the
   8 kHz clip.
6. **Independent decoding is a separate, later check.** Everything above is scored by code we wrote; an MMDVM
   hotspot in the cage is the independent station for M17, POCSAG and DMR.
7. **Unchanged behaviour is re-measured.** Every new image re-runs the long M17 stream (1125 frames) to prove
   ops 0–7 are untouched.
8. **End state recorded:** tag, frequency and power, no leftover updater file, SignalDeck owning the radio.

## 5. Heat

Battery temperature and the phone's thermal zones (`mtktsAP`, the modem PA zones) are logged before, every 5 s
during, and for three minutes after any key longer than 30 s or at high power. Stops: battery above 45 °C, the AP
or modem-PA zone above 60 °C, or a rise of more than 2 °C inside 10 s. One long or high-power key at a time, with
the zone back within 1 °C of its pre-key value before the next. Measured on the Armor: a 120 s high-power key
raises the AP zone about 11 °C and takes about 17 minutes to return.

## 6. The loader

Proven by five loads: an image over itself (tag plus a 4 KiB read-back sample), the factory image (tag plus a
clean tone), the image again, a transfer deliberately closed half way followed by a full load whose first knock
got the prompt, and silent boot captures. The failure on the way (an ordinary command written onto the port
mid-transfer) became the rule that nothing else touches the port during a load.

## 7. Process

- **Two agents, one mailbox.** A builder agent runs the bench and writes `results.md`; a reviewer agent reads
  every commit, writes `reviews.md`, and sets the next step with its pass criteria in `HANDOFF.md`. A step ends
  with its report, never with a commit of fixes. Reviews re-run host tests and recompute hashes themselves.
- **Owner decisions are written down** with the date (time-out ceiling, heat stops, which images are published).
- **Nothing that identifies a person** goes into a repository, including bench logs: bench callsigns only.
- **Every result carries its timestamp, image hash and end state**, so any number in this repository can be
  traced to the capture that produced it.
