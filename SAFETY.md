# Safety: what loading module firmware means, and what protects you

This is the user-facing version of the loader contract (`phonedmrapp/radio_firmware/plan-loader-safety.md`).
SignalDeck's Module firmware page implements it; this page explains it.

## The facts

- **The image goes into the radio module's flash and stays there** across app restarts, phone reboots and module
  power-cycles, until another image is loaded.
- **Loading replaces the whole application image.** The module's bootloader, which accepts the next load, lives
  below the image and is not written, so a module with a broken image can still be reloaded.
- **The bootloader checks nothing** (no signature, no checksum beyond the transfer's own). The hash checks SignalDeck
  does before sending are the only guard against a wrong file.
- **A stock module cannot be read back.** The stock firmware has no command that returns its flash, so the backup
  is the vendor's own copy, which the stock app carries on your phone. Images from this project can be read back
  (opcode 12), and SignalDeck verifies a sample after every load.

## What SignalDeck does before it sends a byte

1. **Identity three ways:** the module's version string, the hash and embedded version of the stock app's firmware
   asset on your phone, and the phone model with the stock app's package. All three must agree with one row of the
   catalogue, or the load is refused and you are told why.
2. **Backup first:** the stock app's own copy is extracted, hash-checked and saved (app storage plus
   `Download/DMR/Firmware/`) before any other image is written. No modified image is loaded without a verified
   factory copy on the phone.
3. **Pre-flight:** module answering, radio idle, stock app paused, battery above 40 % and charging or above 60 %,
   the file's hash in the catalogue, the backup present.
4. **Nothing else touches the port** while a load runs; the rest of the app shows "radio busy".

## What it does after

- Power-cycles the module, reads the version tag and compares it with the image's. **On a mismatch it restores the
  factory image at once.**
- Reads a flash sample back on images that support it and restores the factory image if it differs.
- Writes every step to the history and the device report.

## Recovery

If the module no longer answers at all but still answers the update prompt, the page offers the factory image only,
from your saved copy or from this repository's catalogue, with a warning. That is the "I need a fresh copy" case.

## What is never offered

Band-limit or power changes; any file whose hash is not in the signed catalogue; any image built for a different
base firmware than the one your module runs.
