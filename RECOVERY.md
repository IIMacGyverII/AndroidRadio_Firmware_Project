# Recovery: when the radio module no longer answers

Read `SAFETY.md` first if you have not. This page is for the moment something has gone wrong.

## How to tell what state you are in

| What you see | What it means |
|---|---|
| SignalDeck's Device page shows a module version | The module runs and answers. Nothing here is needed; load the factory image from the Module firmware page if you want the stock behaviour back. |
| No version, the module "has not answered", but the Module firmware page's recovery mode offers the factory image | The application image is broken or absent, the bootloader is intact. This page is for you. |
| No version, and recovery mode reports "no bootloader prompt" after three attempts | The module did not enter update mode. See "If the knock gets no prompt" below. |

The bootloader lives below the application image in the module's flash and is never written by a load, so a bad
or interrupted load leaves it intact. Every recovery below relies on that.

## 1. Recovery from SignalDeck (the normal way)

1. Charge the phone (above 40 % and charging, or above 60 %), keep the stock radio app paused, stop anything that
   uses the radio.
2. Device → Module firmware. With a silent module the page shows only the factory image and a warning.
3. The factory copy comes from your phone's own saved backup (`Download/DMR/Firmware/factory-…bin`, taken from
   your stock app when the page was first opened) or, if that is gone, from this repository's catalogue.
4. Load. The page power-cycles the module with the transmit key held, sends the image, power-cycles again and
   reads the version. "DMR003.UV4T.V022" means you are back to stock.

If the page refuses with a reason, the reason is the fix: charge, pause the stock app, or put the factory file
back under `Download/DMR/Firmware/`.

## 2. Recovery with the stock app (if SignalDeck cannot run)

The stock radio app (PriInterPhone on the Armor 26 Ultra) carries the factory image and an updater:

1. Close SignalDeck and re-enable the stock app.
2. Place the factory image at `/sdcard/DMR/DMRDEBUG.bin` (the updater prefers that file over its built-in copy;
   it must be the exact factory image, check the hash with `scripts/verify_image.py` or `sha256sum`).
3. Open the stock app's firmware update; it performs the same knock and transfer.
4. Delete `/sdcard/DMR/DMRDEBUG.bin` afterwards, or the updater will keep using it.

## 3. If the knock gets no prompt

The knock is a power-cycle with the transmit key held, done through two GPIO nodes. No prompt usually means one of:

- the GPIO nodes are not writable (root was lost, or a different phone whose nodes differ): check the device page;
- the serial port is held by another process (the stock app running at the same time): stop it and retry;
- the module has no power (a hardware or cable fault): nothing in software recovers that.

Retry once after a phone reboot. If there is still no prompt, stop, collect a SignalDeck device report, and open an
issue with it; do not improvise with other images.

## What not to do

- Do not load an image whose hash is not in the catalogue "to see if it helps".
- Do not interrupt a recovery load; it takes about four minutes, and the page shows every phase.
- Do not try other phones' images. The identity checks exist because the modules differ.
