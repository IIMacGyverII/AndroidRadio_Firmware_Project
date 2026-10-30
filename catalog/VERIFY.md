# Verifying the catalogue and an image yourself

You do not have to trust the app, or this repository's hosting, to know that a file is what it claims to be.
The catalogue is signed, and every image is named by its SHA-256.

## The signing key

`public_key.pem` (also `public_key.b64`) is the ECDSA P-256 public key whose private half signs
`firmware.json`. It is the same key built into SignalDeck for its profile list.

SHA-256 fingerprint of the key (DER, SubjectPublicKeyInfo):

```
cb:b2:9f:46:3b:f8:1e:43:85:d6:99:d9:44:58:00:85:6f:b2:23:f1:0b:91:40:43:d2:08:83:74:c2:e8:cd:cd
```

Check it against SignalDeck's source (`ProfileRegistry.PUBLIC_KEY`) or against this page as published at a date
you trust. A key that does not match this fingerprint is not ours.

### The firmware key (catalogue serial 6 and later)

`public_key_firmware.pem` (also `public_key_firmware.b64`) signs every catalogue from serial 6 on, the first one with a released image. It is a separate key from the profile-list key above, created 2026-10-30, and built into SignalDeck from beta.22.

SHA-256 fingerprint (DER, SubjectPublicKeyInfo):

```
49:cc:c9:d6:bb:3f:c1:1e:61:a7:44:38:02:b8:18:5b:eb:d7:fe:fd:cd:fd:d0:95:52:66:63:2a:08:0c:2f:01
```

`scripts/verify_catalog.py` picks the key from the catalogue's serial; pass a key path to force one.

## Check the catalogue's signature

With Python (`pip install cryptography`):

```
python scripts/verify_catalog.py            # uses catalog/firmware.json, .sig and public_key.pem
```

With OpenSSL:

```
base64 -d catalog/firmware.json.sig > sig.der
openssl dgst -sha256 -verify catalog/public_key.pem -signature sig.der catalog/firmware.json
```

Both print a success line only when the file is byte for byte the one that was signed. Any edit, even a space,
fails the check.

## Check an image

```
sha256sum firmware/<device>/<tag>/<tag>.bin
python scripts/verify_image.py path/to/file.bin
```

The script also reads the version string inside the file at the module's known offset and compares it with the
catalogue row. A file whose hash is not in the catalogue is not an image, whatever its name says.

## What verification does not tell you

That an image is right for your phone. That is the loader's identity check (module version string, your stock
app's firmware asset, the phone model and stock package), described in `../SAFETY.md`.
