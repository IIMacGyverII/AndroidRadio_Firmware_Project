#!/usr/bin/env python3
"""Verify catalog/firmware.json against its .sig and the published public key.

  python scripts/verify_catalog.py [catalog/firmware.json] [catalog/public_key.pem]

Exit 0 and a success line only when the signature is valid for the file byte for byte and the key's SHA-256
fingerprint is printed for comparison with catalog/VERIFY.md. Needs `pip install cryptography`.
"""
import base64
import hashlib
import json
import sys
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

ROOT = Path(__file__).resolve().parent.parent
cat = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "catalog" / "firmware.json"
key_path = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "catalog" / "public_key.pem"

data = cat.read_bytes()
sig = base64.b64decode(Path(str(cat) + ".sig").read_text().strip())
pub = serialization.load_pem_public_key(key_path.read_bytes())
der = pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
fp = hashlib.sha256(der).hexdigest()
print("key fingerprint:", ":".join(fp[i:i + 2] for i in range(0, 64, 2)))
try:
    pub.verify(sig, data, ec.ECDSA(hashes.SHA256()))
except InvalidSignature:
    print(f"{cat}: SIGNATURE INVALID")
    sys.exit(1)
doc = json.loads(data)
print(f"{cat}: signature valid, format {doc.get('format')}, serial {doc.get('serial')}, {len(doc.get('images', []))} image(s), "
      f"{sum(len(d.get('variants', [])) for d in doc.get('variants', []))} variant(s)")
