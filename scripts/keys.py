"""Which key signs which catalogue serial. See catalog/KEYS.md.

Serials below FIRMWARE_KEY_FROM_SERIAL were signed with the shared profile-list key; from it on, the firmware key
signs. SignalDeck carries the same number: builds from beta.22 verify serial >= this number with the firmware key,
older builds know only the profile key and keep the last catalogue they verified.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIRMWARE_KEY_FROM_SERIAL = 6   # the catalogue that first lists a released image (FW57, owner 2026-10-30)

PRIVATE = {
    "profile": Path(os.path.expanduser("~")) / ".signaldeck" / "profile_signing_key.pem",
    "firmware": Path(os.path.expanduser("~")) / ".signaldeck" / "firmware_signing_key.pem",
}
PUBLIC = {
    "profile": ROOT / "catalog" / "public_key.pem",
    "firmware": ROOT / "catalog" / "public_key_firmware.pem",
}


def key_for(serial: int) -> str:
    return "firmware" if serial >= FIRMWARE_KEY_FROM_SERIAL else "profile"
