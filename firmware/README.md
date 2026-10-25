# Firmware images

`firmware/<device>/<tag>/` holds one image: `<tag>.bin`, `manifest.json`, `README.md`. The folder is named after the
version string the image reports (`0x34`), and the manifest is what the catalogue is built from.

## Manifest fields

| Field | Meaning |
|---|---|
| `tag` | the version string inside the image and the folder name |
| `file`, `size`, `sha256`, `md5` | the file and its identity; `build_catalog.py --check` verifies all three against the bytes |
| `device` | the `devices/` folder this image is for |
| `model` | the `Build.MODEL` the loader compares against |
| `module` | the `modules/` folder (decides where the version string sits) |
| `base` | the stock image this one was built on; a stock image names itself |
| `factory` | true for the stock image of a device (the restore target) |
| `readBack` | true when the image answers opcode 12, so a load can be verified by reading flash back |
| `stockPackage`, `stockVersion` | the stock app whose firmware asset is the base |
| `summary` | one paragraph a user reads on the loader page |
| `changes` | the list of what the image changes against its base |
| `transmitLimitSeconds` | the module's own time-out on this image (0 = off) |
| `persistsAcrossReboot` | always true on this module family |
| `status` | `stock` or `released`; bench and beta images are never committed here |
| `measured` | date of the bench proof |
| `builtFrom` | repository, commit and script that reproduce the bytes; for a stock image, the package, version and asset path it was taken from |
| `results` | where the measurements are written up |

## Rules

- A stock image is added byte for byte from the stock app's asset, with the asset's hash in `builtFrom`.
- A modified image is added only once the owner releases it, when a clean checkout of the named commit reproduces
  its hash and its results are linked. Bench and beta images stay in phonedmrapp.
- Images never change band limits or power. Images never key the radio at boot.
- Removing or altering a device's factory image is never done.
