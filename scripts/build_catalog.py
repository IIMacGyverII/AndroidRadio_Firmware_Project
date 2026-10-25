#!/usr/bin/env python3
"""Build catalog/firmware.json from every firmware/*/*/manifest.json.

  python scripts/build_catalog.py --check            # verify every manifest against its file, write nothing
  python scripts/build_catalog.py --serial N         # verify, then write the catalogue with serial N

A manifest is accepted only when its file exists, its size, sha256 and md5 match the file, the version tag at the
module's tag offset matches "tag", and its folder is named after the tag. The catalogue is never edited by hand.
"""
import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://raw.githubusercontent.com/IIMacGyverII/AndroidRadio_Firmware_Project/main/"
TAG_AT = {"hr-c7000": 0x38464}   # file offset of the 16-byte version string, per module family

REQUIRED = ["tag", "file", "size", "sha256", "md5", "device", "model", "module", "base", "factory", "readBack",
            "stockPackage", "stockVersion", "summary", "changes", "transmitLimitSeconds", "persistsAcrossReboot",
            "status", "measured", "builtFrom", "results"]


def tag_of(data: bytes, module: str) -> str:
    off = TAG_AT.get(module)
    if off is None or len(data) < off + 16:
        return ""
    raw = data[off:off + 16]
    return raw.split(b"\0", 1)[0].decode("ascii", "replace").strip()


def check(manifest_path: Path) -> dict:
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED if k not in m]
    if missing:
        raise SystemExit(f"{manifest_path}: missing {missing}")
    folder = manifest_path.parent
    if folder.name != m["tag"]:
        raise SystemExit(f"{manifest_path}: folder {folder.name} is not the tag {m['tag']}")
    if folder.parent.name != m["device"]:
        raise SystemExit(f"{manifest_path}: device folder {folder.parent.name} is not {m['device']}")
    f = folder / m["file"]
    if not f.is_file():
        raise SystemExit(f"{manifest_path}: {m['file']} is missing")
    data = f.read_bytes()
    if len(data) != m["size"]:
        raise SystemExit(f"{manifest_path}: size {len(data)} is not {m['size']}")
    sha = hashlib.sha256(data).hexdigest()
    md5 = hashlib.md5(data).hexdigest()
    if sha != m["sha256"].lower():
        raise SystemExit(f"{manifest_path}: sha256 {sha} is not {m['sha256']}")
    if md5 != m["md5"].lower():
        raise SystemExit(f"{manifest_path}: md5 {md5} is not {m['md5']}")
    tag = tag_of(data, m["module"])
    if tag != m["tag"]:
        raise SystemExit(f"{manifest_path}: the file's version string is {tag!r}, not {m['tag']}")
    m["url"] = BASE_URL + f.relative_to(ROOT).as_posix()
    return m


ALLOWED_STATUS = {"stock", "released"}   # bench and beta images are never committed here (owner, 2026-10-25)


def variants() -> list:
    """Every devices/*/variants.json, folded into the catalogue so the app can name a known-but-unsupported variant."""
    out = []
    for p in sorted((ROOT / "devices").glob("*/variants.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("device") != p.parent.name:
            raise SystemExit(f"{p}: device {d.get('device')} is not the folder {p.parent.name}")
        for v in d.get("variants", []):
            for k in ("moduleVersion", "stockApp", "assetSha256", "assetSize", "supportedBase", "reports", "source"):
                if k not in v:
                    raise SystemExit(f"{p}: variant missing {k}")
        out.append(d)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="verify only")
    ap.add_argument("--serial", type=int, help="write the catalogue with this serial")
    ap.add_argument("--out", type=Path, help="write to this path instead of catalog/firmware.json (CI rebuild)")
    ap.add_argument("--force", action="store_true", help="allow a serial that is not above the published one (CI rebuild)")
    a = ap.parse_args()
    if not a.check and a.serial is None:
        ap.error("--check or --serial N")
    entries = [check(p) for p in sorted((ROOT / "firmware").glob("*/*/manifest.json"))]
    for e in entries:
        if e["status"] not in ALLOWED_STATUS:
            raise SystemExit(f"{e['device']}/{e['tag']}: status {e['status']!r} is not allowed here (stock or released only)")
    vs = variants()
    print(f"{len(entries)} image(s) verified, {sum(len(d['variants']) for d in vs)} variant(s) from {len(vs)} device(s)")
    for e in entries:
        print(f"  {e['device']}/{e['tag']}  {e['sha256'][:12]}  {e['status']}")
    if a.check:
        return
    out = a.out or (ROOT / "catalog" / "firmware.json")
    published = ROOT / "catalog" / "firmware.json"
    if published.exists() and not a.force:
        old = json.loads(published.read_text(encoding="utf-8"))
        if a.serial <= old.get("serial", 0):
            raise SystemExit(f"serial {a.serial} is not above the published {old.get('serial')}")
    doc = {"format": 1, "serial": a.serial, "generated": datetime.date.today().isoformat(), "base": BASE_URL,
           "images": entries, "variants": vs}
    out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    if out == published:
        sig = Path(str(out) + ".sig")
        if sig.exists():
            sig.unlink()
        print(f"wrote {out} serial {a.serial}; now run scripts/sign_catalog.py")
    else:
        print(f"wrote {out} serial {a.serial}")


if __name__ == "__main__":
    main()
