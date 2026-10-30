#!/usr/bin/env python3
"""Sign catalog/firmware.json with the SignalDeck profile-list key.

  python scripts/sign_catalog.py [catalog/firmware.json]

Writes <file>.sig (base64 DER ECDSA P-256 / SHA-256), the scheme SignalDeck's ProfileRegistry verifies with the
public key built into the app. The private key is ~/.signaldeck/profile_signing_key.pem and is never committed.
Refuses a file that is not valid JSON with format 1 and an integer serial.
"""
import base64
import json
import os
import sys

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "catalog", "firmware.json")
key_path = os.path.join(os.path.expanduser("~"), ".signaldeck", "profile_signing_key.pem")
data = open(path, "rb").read()
doc = json.loads(data)
assert doc.get("format") == 1 and isinstance(doc.get("serial"), int), "needs format 1 and an integer serial"
key = serialization.load_pem_private_key(open(key_path, "rb").read(), None)
sig = key.sign(data, ec.ECDSA(hashes.SHA256()))
open(path + ".sig", "w").write(base64.b64encode(sig).decode())
print("signed", path, "serial", doc["serial"], "-", len(doc.get("images", [])), "images")
