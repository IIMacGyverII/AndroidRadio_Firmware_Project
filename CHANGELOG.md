# Changelog

Newest first. One entry per change that a user of SignalDeck or a reader of the repository would notice.

## 2026-10-30 — SignalDeck 1.0.0-beta.22 published; FW57 is now offered

- SignalDeck beta.22 (versionCode 121, release asset sha256 `62b6ad8632aedbb275fe44a0a2f65f0b6b0e5d85a2cea117cfc5fa5d0382e62a`) is the first build that verifies catalogue serial 6 (firmware key) and offers `DMR003.FW57.V022` (`released-min` 121). Tested end to end before publishing, on an Armor 26 Ultra starting from the factory image, through the app's own Module firmware page: the catalogue fetched and verified, FW57 downloaded and checked, pre-flight, load (370/370 blocks), module reporting FW57; FM, DMR, M17 and Morse transmissions decoded by an independent receiver; Restore back to the factory image. Records: phonedmrapp `radio_firmware/results.md` (2026-10-30, 13:37 and 13:45).

## 2026-10-30 — DMR003.FW57.V022 released for the Armor 26 Ultra (catalogue serial 6)

- `firmware/ulefone-armor-26-ultra/DMR003.FW57.V022/`: the first released modified image (owner, 2026-10-30). Adds the module transmitter (M17, POCSAG, FT8, RTTY, Morse) and keeps FM, CTCSS, SSTV and DMR as shipped. Reproducible from phonedmrapp `a7943723` (`tools/fw-patch/test_repro_fw57.py`, 19 steps from the factory image). Measured rows in its README.
- Catalogue serial 6, the first signed with the firmware key. FW57 is `released-min` with `minAppVersionCode` 121: offered only by SignalDeck beta.22 and newer. Older builds cannot verify serial 6 and keep serial 5.
- Known open: promiscuous DMR receive does not admit out-of-list calls yet (not used by SignalDeck beta.22); slot 1 DMR receive not covered by the bench.

## 2026-10-30 — A separate firmware signing key; the released-min status

- **Firmware key** (owner, 2026-10-30, before the first released image): `catalog/public_key_firmware.pem` / `.b64`, fingerprint `49:cc:c9:d6:bb:3f:c1:1e:61:a7:44:38:02:b8:18:5b:eb:d7:fe:fd:cd:fd:d0:95:52:66:63:2a:08:0c:2f:01`. It signs catalogue serial 6 and later; serials 1–5 stay signed with the shared profile-list key. `scripts/keys.py` holds the switch; `sign_catalog.py` and `verify_catalog.py` choose the key from the serial. SignalDeck carries both public keys from beta.22, so older builds keep the last catalogue they could verify.
- **`released-min`** catalogue status with `minAppVersionCode` (SignalDeck PR 144): a released image offered only to new enough app builds. FW57 will use it (needs SignalDeck beta.22). `build_catalog.py` refuses it without a positive minimum.
- The published catalogue (serial 5) is unchanged.

## 2026-10-26 — Atom XL module image (research copy)

- `firmware/unihertz-atom-xl/DMR006.U4A.V076/`: the module image an Atom XL keeps on its vendor partition, byte for
  byte, with manifest and README. It is older than the V082 the phone's module runs, so it is `factory: false` and
  SignalDeck does not offer it for loading.
- `devices/unihertz-atom-xl/`: the V076 variant and where it came from.
- `scripts/build_catalog.py`: a manifest may name its own `tagOffset` (this image's version string is at `0x33410`).
- Catalogue serial 5.

## 2026-10-25 — Registry, keys, recovery, templates, CI

- Variant registry: `devices/<device>/variants.json` for every module version and stock asset seen on a model,
  folded into the signed catalogue (`variants`), with `devices/VARIANTS.md`.
- Public signing key published (`catalog/public_key.pem`, fingerprint in `catalog/VERIFY.md`) with verification
  instructions; `catalog/KEYS.md` records custody, the planned separate firmware key, and rotation.
- `RECOVERY.md` for a module that no longer answers.
- `devices/TEMPLATE.md` and `devices/device.schema.json`; GitHub issue forms and a pull-request checklist.
- CI (`.github/workflows/check.yml`): manifests match their files, the committed catalogue matches the manifests,
  the signature verifies, the agent files are mirrored, no bench or beta image is present.
- `SAFETY.md`: the owner's rule for loading your own image (Advanced switch, off by default, two confirmations,
  hash typed, all other checks kept).
- `research/METHODS.md`: the bench, the reading, the build, the test order, heat, the loader proofs, the process.
- Catalogue serial 3 (serial 2 was signed over CRLF bytes and never valid on a Linux checkout; the builder now writes LF and `.gitattributes` keeps the catalogue files byte-exact).

## 2026-10-25 — Repository created

- Layout: `firmware/`, `catalog/`, `devices/`, `modules/`, `research/`, `scripts/`, with `SAFETY.md` and `NOTICE.md`.
- Images: Ulefone Armor 26 Ultra stock `DMR003.UV4T.V022` with manifest and provenance. Bench and beta images are
  not committed here (owner's rule); released images will be.
- Catalogue `firmware.json` serial 1, signed with the SignalDeck profile-list key.
- Devices: Armor 26 Ultra (verified), Armor 20WT, Armor 3WT, Atom XL, Xplore 1, DOOGEE S80 (from reports and stock
  apps, unverified).
- Module: HR-C7000 + AT1846S facts, including update mode and the bootloader handshake.
