#!/usr/bin/env python3
"""Sign catalog/firmware.json with the key its serial calls for (scripts/keys.py).

  python scripts/sign_catalog.py [catalog/firmware.json]

Writes <file>.sig (base64 DER ECDSA P-256 / SHA-256), the scheme SignalDeck verifies with the public keys built
into the app. Serials from keys.FIRMWARE_KEY_FROM_SERIAL on are signed with ~/.signaldeck/firmware_signing_key.pem,
earlier ones with ~/.signaldeck/profile_signing_key.pem. Private keys are never committed.
Refuses a file that is not valid JSON with format 1 and an integer serial.
"""
import base64
import json
import os
import sys

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import keys  # noqa: E402

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "catalog", "firmware.json")
data = open(path, "rb").read()
doc = json.loads(data)
assert doc.get("format") == 1 and isinstance(doc.get("serial"), int), "needs format 1 and an integer serial"
which = keys.key_for(doc["serial"])
key = serialization.load_pem_private_key(open(keys.PRIVATE[which], "rb").read(), None)
sig = key.sign(data, ec.ECDSA(hashes.SHA256()))
open(path + ".sig", "w").write(base64.b64encode(sig).decode())
print("signed", path, "serial", doc["serial"], "with the", which, "key -", len(doc.get("images", [])), "images")
