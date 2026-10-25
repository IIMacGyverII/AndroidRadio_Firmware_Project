# The firmware catalogue

`firmware.json` (+ `firmware.json.sig`) is the list SignalDeck fetches to know which module images exist, for which
device, with which hash, and where to download them. It is **generated** from the manifests under `firmware/` and
**signed** with the same key and scheme as SignalDeck's profile list, so the app verifies both with one public key.

Fetch URL: `https://raw.githubusercontent.com/IIMacGyverII/AndroidRadio_Firmware_Project/main/catalog/firmware.json`
(and `.sig` beside it). Image URLs inside the catalogue point at the raw files under `firmware/`.

## Format

```json
{
  "format": 1,
  "serial": 1,
  "generated": "2026-10-25",
  "base": "https://raw.githubusercontent.com/IIMacGyverII/AndroidRadio_Firmware_Project/main/",
  "images": [ { ...one manifest per image, plus "url" and "device"... } ]
}
```

Each entry carries the manifest fields (`firmware/README.md`): `tag`, `file`, `size`, `sha256`, `md5`, `device`,
`model`, `module`, `base`, `factory`, `readBack`, `stockPackage`, `stockVersion`, `summary`, `changes`,
`transmitLimitSeconds`, `persistsAcrossReboot`, `status`, `measured`, `builtFrom`, `results`, and `url`.

Only stock and released images are listed. SignalDeck offers a row only when the module's version string is the row's `base` (or its `tag`), the phone model and
stock package match, and the phone holds a verified factory copy for that base. A silent module is offered the
factory row only.

## Publishing

1. Add or change an image under `firmware/` with its manifest and README.
2. `python scripts/build_catalog.py --check` (verifies every manifest against its file) then
   `python scripts/build_catalog.py --serial N` with N higher than the current serial.
3. `python scripts/sign_catalog.py` (needs `~/.signaldeck/profile_signing_key.pem`; the key is never in a repository).
4. Commit `catalog/firmware.json` and `catalog/firmware.json.sig` together with the image folder.

Phones ignore a catalogue whose serial is lower than the one they already have, so never publish a lower serial.
