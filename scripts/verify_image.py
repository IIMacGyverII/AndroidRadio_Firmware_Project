#!/usr/bin/env python3
"""Check a local image file against the catalogue.

  python scripts/verify_image.py path/to/image.bin

Prints the catalogue row the file matches (by sha256, size and embedded version tag) or says it is unknown.
Use it before loading anything by hand: a file whose hash is not in the catalogue is not an image.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG_AT = {"hr-c7000": 0x38464}

if len(sys.argv) != 2:
    raise SystemExit(__doc__)
f = Path(sys.argv[1])
data = f.read_bytes()
sha = hashlib.sha256(data).hexdigest()
cat = json.loads((ROOT / "catalog" / "firmware.json").read_text(encoding="utf-8"))
for e in cat["images"]:
    if e["sha256"].lower() == sha and e["size"] == len(data):
        off = TAG_AT.get(e["module"])
        tag = data[off:off + 16].split(b"\0", 1)[0].decode("ascii", "replace").strip() if off else ""
        ok = tag == e["tag"]
        print(f"{f.name}: {e['device']} {e['tag']} ({e['status']}), tag in file {tag!r} {'ok' if ok else 'MISMATCH'}")
        print(f"  {e['summary']}")
        sys.exit(0 if ok else 2)
print(f"{f.name}: sha256 {sha} is not in the catalogue (serial {cat['serial']}). Do not load it.")
sys.exit(1)
