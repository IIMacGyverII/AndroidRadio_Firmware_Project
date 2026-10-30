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
