# Key custody and rotation

## Today

One ECDSA P-256 key signs both SignalDeck's profile list and this firmware catalogue. The private half lives only
on the maintainer's PC (`~/.signaldeck/profile_signing_key.pem`), with an offline backup, and is in no repository.
The public half is `public_key.pem` here and `ProfileRegistry.PUBLIC_KEY` in SignalDeck; fingerprint in `VERIFY.md`.

What it protects: the app accepts a catalogue or profile list only with a valid signature and a serial not lower
than the one it already holds. Control of the GitHub repository or of the download path is therefore not enough to
push an image or a profile to users; the private key is.

## Planned: a separate firmware key

Before the first released image, firmware gets its own key, so a compromise of one list does not reach the other
and the two can be rotated independently:

1. Generate `firmware_signing_key.pem` offline; publish its public half here as `public_key_firmware.pem` with its
   fingerprint.
2. SignalDeck carries both public keys (profile list → profile key, firmware catalogue → firmware key) in a release.
3. From the catalogue serial that follows that release, `sign_catalog.py` uses the firmware key. Older app builds
   verify older serials only, which is the intended effect: an app that does not know the new key does not load
   firmware from the new catalogue.

## Rotation (either key)

If a private key is suspected compromised:

1. Stop signing with it. Publish nothing new under it.
2. Generate the replacement offline; ship a SignalDeck release that trusts the new key and **no longer trusts the
   old one**; publish the new public key and fingerprint here, and note the retirement in `CHANGELOG.md`.
3. Re-sign the current list or catalogue with the new key at a higher serial.
4. Because app releases come from the same GitHub account, that account's two-factor protection and the release
   signing keystore are part of the chain; treat them with the same care as the signing key.

A key is never rotated silently. The fingerprint history stays in this file:

| Key | Fingerprint (SHA-256 of the DER public key) | In use |
|---|---|---|
| profile + firmware (current) | `cb:b2:9f:46:3b:f8:1e:43:85:d6:99:d9:44:58:00:85:6f:b2:23:f1:0b:91:40:43:d2:08:83:74:c2:e8:cd:cd` | since 2026-10-22 (profiles), 2026-10-25 (firmware) |
